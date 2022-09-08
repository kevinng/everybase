import pytz, urllib
from leads.utilities.set_cookie_uuid import set_cookie_uuid
from leads.utilities.get_or_set_cookie_uuid import get_or_create_cookie_uuid
from datetime import datetime
from ratelimit.decorators import ratelimit

from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User as DjangoUser
from django.template.response import TemplateResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from everybase import settings

from common import models as commods
from common.tasks.send_email import send_email
from common.tasks.send_amplitude_event import send_amplitude_event
from common.tasks.identify_amplitude_user import identify_amplitude_user
from common.utilities.get_ip_address import get_ip_address

from relationships import forms, models
from relationships.tasks import send_email_code
from relationships.tasks import send_whatsapp_code
from relationships.utilities.are_phone_numbers_same import are_phone_numbers_same
from relationships.utilities.email_exists import email_exists
from relationships.utilities.get_or_create_phone_number import get_or_create_phone_number
from relationships.utilities.get_or_create_email import get_or_create_email
from relationships.utilities.phone_number_exists import phone_number_exists
from relationships.utilities.use_email_code import use_email_code
from relationships.utilities.use_whatsapp_code import use_whatsapp_code
from relationships.utilities.user_uuid_exists import user_uuid_exists
from relationships.constants import email_purposes, whatsapp_purposes

MESSAGE_KEY__PROFILE_UPDATE_SUCCESS = 'MESSAGE_KEY__PROFILE_UPDATE_SUCCESS'
MESSAGE_KEY__EMAIL_UPDATE_TRY_AGAIN = 'MESSAGE_KEY__EMAIL_UPDATE_TRY_AGAIN'
MESSAGE_KEY__EMAIL_UPDATE_SUCCESS = 'MESSAGE_KEY__EMAIL_UPDATE_SUCCESS'
MESSAGE_KEY__PHONE_NUMBER_UPDATE_TRY_AGAIN = 'MESSAGE_KEY__PHONE_NUMBER_UPDATE_TRY_AGAIN'
MESSAGE_KEY__PHONE_NUMBER_UPDATE_SUCCESS = 'MESSAGE_KEY__PHONE_NUMBER_UPDATE_SUCCESS'

# Helper functions

def _append_next(url, next):
    """Append next URL to input URL as a GET parameter."""
    if next is not None and next.strip() != '':
        url += f'&next={next}'
    return url

def _pass_next(params, next):
    """Add next URL to params dictionary."""
    if next is not None and next.strip() != '':
        params['next'] = next
    return params

def _next_or_else_response(next, default):
    """Return HTTPRedirectResponse to next if it's not none/empty, or default otherwise."""
    if next is not None and next.strip() != '':
        return HttpResponseRedirect(next)
    else:
        return HttpResponseRedirect(default)

# Named 'log_in' and not 'login' to prevent clash with Django login
@ratelimit(key='user_or_ip', rate='30/h', block=True, method=['POST'])
def log_in(request):
    # if request.user.is_authenticated:
        # return HttpResponseRedirect(reverse('home')) # Go home if authenticated
    
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = form.user
            if form.email is not None:
                send_email_code.send_email_code(user, email_purposes.LOGIN)
                url = reverse('confirm_email_login')
            elif form.phone_number is not None:
                send_whatsapp_code.send_whatsapp_code(user, whatsapp_purposes.LOGIN)
                url = reverse('confirm_whatsapp_login')

            url += f'?uuid={user.uuid}'
            return HttpResponseRedirect(_append_next(url, form.cleaned_data.get('next')))
    else:
        initial = {}
        login_str = request.GET.get('login')
        if login_str is not None:
            initial['email_or_phone_number'] = login_str

        form = forms.LoginForm(initial=initial)

    params = _pass_next({'form': form}, request.GET.get('next'))
    return TemplateResponse(request, 'relationships/login.html', params)

def confirm_whatsapp_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home')) # Go home if authenticated
    
    if request.method == 'POST':
        form = forms.ConfirmWhatsAppLoginForm(request.POST)
        if form.is_valid():
            user = form.user
            use_whatsapp_code(user)
            dju = authenticate(user.django_user.username) # Passwordless
            if dju is not None:
                login(request, dju)

                send_amplitude_event.delay(
                    'account - logged in',
                    user_uuid=form.user.uuid,
                    ip=get_ip_address(request),
                    event_properties={
                        'login type': 'whatsapp',
                        'next': form.cleaned_data.get('next')
                    }
                )

                cookie_uuid, _ = get_or_create_cookie_uuid(request)
                models.LoginAction.objects.create(
                    user=user,
                    cookie_uuid=cookie_uuid,
                    type='whatsapp'
                )
                response = _next_or_else_response(form.cleaned_data.get('next'), reverse('home'))
                return set_cookie_uuid(response, cookie_uuid)

    elif request.method == 'GET':
        uuid = request.GET.get('uuid')
        user = user_uuid_exists(uuid)
        if user is None:
            return HttpResponseRedirect(reverse('login')) # Unlikely error (e.g., bug or user temperage). Direct to login. No need for message.

        form = forms.ConfirmWhatsAppLoginForm(initial={
            'uuid': uuid,
            'next': request.GET.get('next'),
            'phone_number': f'{user.phone_number.country_code} {user.phone_number.national_number}'
        })
    
    return TemplateResponse(request, 'relationships/confirm_whatsapp_login.html', {'form': form})

def select_country(request):
    return TemplateResponse(request, 'relationships/select_country.html', None)

def register(request):
    # if request.user.is_authenticated:
        # return HttpResponseRedirect(reverse('home')) # Go home if authenticated

    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            # Create Everybase user
            cookie_uuid, _ = get_or_create_cookie_uuid(request)
            user = models.User.objects.create(
                register_cookie_uuid=cookie_uuid,
                registered=datetime.now(pytz.timezone(settings.TIME_ZONE)),
                email=get_or_create_email(form.cleaned_data.get('email')),
                phone_number=get_or_create_phone_number(form.cleaned_data.get('phone_number')),
                country=commods.Country.objects.get(programmatic_key=form.cleaned_data.get('country')),
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
                enable_whatsapp=False # Default, require verification to enable
            )

            # Create Django user and associate it
            user.django_user, _ = DjangoUser.objects.get_or_create(username=str(user.uuid))
            user.save()

            # Authenticate passwordlessly
            dju = authenticate(user.django_user.username)
            if dju is not None:
                login(request, dju)

            # Send welcome email
            send_email.delay(
                render_to_string('relationships/email/welcome_subject.txt', {}),
                render_to_string('relationships/email/welcome.txt', {}),
                'friend@everybase.co',
                [user.email.email]
            )

            identify_amplitude_user.delay(
                user_id=user.uuid,
                user_properties={
                    'country': user.country.programmatic_key,
                    'phone number country code': user.phone_number.country_code
                }
            )

            send_amplitude_event.delay(
                'account - registered',
                user_uuid=user.uuid,
                ip=get_ip_address(request),
                event_properties={
                    'country': user.country.programmatic_key,
                    'phone number country code': user.phone_number.country_code
                }
            )

            # Verify WhatsApp number if user enabled WhatsApp
            if form.cleaned_data.get('enable_whatsapp') == True:
                return HttpResponseRedirect(reverse('users:verify_whatsapp'))

            return _next_or_else_response(form.cleaned_data.get('next'), reverse('home'))
    else:
        form = forms.RegisterForm()

    params = _pass_next({
        'form': form,
        'countries': commods.Country.objects.annotate(
            num_users=Count('users_w_this_country')).order_by('-num_users')
    }, request.GET.get('next'))        
    return TemplateResponse(request, 'relationships/register.html', params)

# User will be authenticated coming from register view
# @login_required
def verify_whatsapp(request):
    # user = request.user.user
    # kwargs = {'user': user}

    # if request.method == 'POST':
    #     form = forms.VerifyWhatsAppForm(request.POST, **kwargs)
    #     if form.is_valid():
    #         use_whatsapp_code(user)
    #         user.enable_whatsapp = True # Enable after verification, otherwise False.
    #         user.save()
    #         return _next_or_else_response(form.cleaned_data.get('next'), reverse('home'))
    # else:
    #     send_whatsapp_code.send_whatsapp_code(user, whatsapp_purposes.UPDATE_PHONE_NUMBER)
    #     form = forms.VerifyWhatsAppForm(**kwargs)

    # params = _pass_next({'form': form}, request.GET.get('next'))
    return TemplateResponse(request, 'relationships/verify_whatsapp.html', None)

# Don't name profile settings function 'settings', it conflicts with everybase.settings.
@login_required
def profile_settings(request):
    





    user = request.user.user
    kwargs = {'user': user}

    # Default SettingsForm values to user's existing values
    inputs = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'country': user.country.programmatic_key if user.country is not None else 'country_not_set',
        'enable_whatsapp': user.enable_whatsapp
    }

    # Default email if user's email is set
    if user.email is not None:
        inputs['email'] = user.email.email

    # Default phone number if user's phone number is set
    if user.phone_number is not None:
        inputs['phone_number'] = f'+{user.phone_number.country_code} {user.phone_number.national_number}'

    if request.method == 'POST':
        # Override form with relevant values depending on the button clicked, so only relevant fields are updated.
        if request.POST.get('update_profile') == 'update_profile':
            inputs['first_name'] = request.POST.get('first_name')
            inputs['last_name'] = request.POST.get('last_name')
            inputs['country'] = request.POST.get('country')
            inputs['update_profile'] = 'update_profile'

        elif request.POST.get('update_email') == 'update_email':
            inputs['email'] = request.POST.get('email')
            inputs['update_email'] = 'update_email'

        elif request.POST.get('update_phone_number') == 'update_phone_number':
            inputs['phone_number'] = request.POST.get('phone_number')
            inputs['enable_whatsapp'] = request.POST.get('enable_whatsapp')
            inputs['update_phone_number'] = 'update_phone_number'

        form = forms.SettingsForm(inputs, **kwargs)

        if form.is_valid():
            if request.POST.get('update_profile') == 'update_profile':
                user = request.user.user

                # Record old values
                old_first_name = user.first_name
                old_last_name = user.last_name
                old_country_key = user.country.programmatic_key if user.country is not None else None

                user.first_name = form.cleaned_data.get('first_name')
                user.last_name = form.cleaned_data.get('last_name')
                
                country_key = form.cleaned_data.get('country')
                country = None
                if not (country_key == 'country_not_set' or country_key is None or (type(country_key) == str and country_key.strip() == '')):
                    try:
                        country = commods.Country.objects.get(programmatic_key=country_key)
                    except commods.Country.DoesNotExist:
                        pass
                user.country = country
                user.save()
                messages.add_message(request, messages.SUCCESS, MESSAGE_KEY__PROFILE_UPDATE_SUCCESS)

                user_properties = {}
                if user.country is not None:
                    user_properties['country'] = user.country.programmatic_key
                if user.phone_number is not None:
                    user_properties['phone number country code'] = user.phone_number.country_code

                identify_amplitude_user.delay(
                    user_id=user.uuid,
                    user_properties=user_properties
                )

                amplitude_event_properties = {}
                amplitude_event_properties['old first name'] = old_first_name
                amplitude_event_properties['new first name'] = user.first_name
                amplitude_event_properties['old last name'] = old_last_name
                amplitude_event_properties['new last name'] = user.last_name
                if old_country_key is not None:
                    amplitude_event_properties['old country'] = old_country_key
                if user.country is not None:
                    amplitude_event_properties['new country'] = user.country.programmatic_key

                send_amplitude_event.delay(
                    'account - updated profile',
                    user_uuid=user.uuid,
                    ip=get_ip_address(request),
                    event_properties=amplitude_event_properties
                )

            elif request.POST.get('update_email') == 'update_email':
                if (user.email is None or user.email.email != form.cleaned_data.get('email').strip()):
                    return HttpResponseRedirect(f"{reverse('users:update_email')}?email={form.cleaned_data.get('email')}")

            elif request.POST.get('update_phone_number') == 'update_phone_number':
                phone_number = form.cleaned_data.get('phone_number')
                enable_whatsapp = form.cleaned_data.get('enable_whatsapp')

                encph = urllib.parse.quote(str(phone_number)) # Encode phone number so the + symbol is passed safely
                verification_url = f"{reverse('users:update_phone_number')}?phone_number={encph}&enable_whatsapp={enable_whatsapp}"

                if user.phone_number is None or not are_phone_numbers_same(user.phone_number, phone_number):
                    # Require verification even if the user wants to disable WhatsApp
                    return HttpResponseRedirect(verification_url)
                elif user.enable_whatsapp != enable_whatsapp:
                    if not enable_whatsapp:
                        # Do not require verification to disable WhatsApp if phone number is unchanged
                        user.enable_whatsapp = False
                        user.save()
                        messages.add_message(request, messages.SUCCESS, MESSAGE_KEY__PHONE_NUMBER_UPDATE_SUCCESS)
                    else:
                        # Require verification to enable WhatsApp even if phone number is the same
                        return HttpResponseRedirect(verification_url)

    else:
        form = forms.SettingsForm(initial=inputs, **kwargs)

    return TemplateResponse(request, 'relationships/settings.html', {
        'form': form,
        'countries': commods.Country.objects.annotate(
            num_users=Count('users_w_this_country')).order_by('-num_users')
    })

@login_required
def update_email(request):
    user = request.user.user
    kwargs = {'user': user}

    if request.method == 'POST':
        form = forms.UpdateEmailForm(request.POST, **kwargs)
        if form.is_valid():
            # Validate email, in case it has been tempered
            email = form.cleaned_data.get('email')
            old_email = user.email.email if user.email is not None else None
            if not email_exists(email):
                user.email, _ = models.Email.objects.get_or_create(email=email)
                user.save()
                messages.add_message(request, messages.SUCCESS, MESSAGE_KEY__EMAIL_UPDATE_SUCCESS)

                event_properties = {}
                if old_email is not None:
                    event_properties['old email'] = old_email
                event_properties['new email'] = user.email.email
            
                send_amplitude_event.delay(
                    'account - updated email',
                    user_uuid=user.uuid,
                    ip=get_ip_address(request),
                    event_properties=event_properties
                )
            else:
                messages.add_message(request, messages.ERROR, MESSAGE_KEY__EMAIL_UPDATE_TRY_AGAIN)

            return HttpResponseRedirect(reverse('users:settings'))
    else:
        email = request.GET.get('email')

        send_email_code.send_email_code(user, email_purposes.UPDATE_EMAIL, email)
        form = forms.UpdateEmailForm(initial={'email': email}, **kwargs)
        
    return TemplateResponse(request, 'relationships/confirm_email_change.html', {'form': form})

def update_phone_number(request):
    user = request.user.user
    kwargs = {'user': user}

    if request.method == 'POST':
        form = forms.UpdatePhoneNumberForm(request.POST, **kwargs)
        if form.is_valid():
            # Validate phone number, in case it has been tempered
            phone_number = form.cleaned_data.get('phone_number')
            enable_whatsapp = form.cleaned_data.get('enable_whatsapp')

            # Record old values
            old_phone_number = user.phone_number.value() if user.phone_number is not None else None
            old_enable_whatsapp = user.enable_whatsapp

            if phone_number_exists(phone_number) is not None:
                # User is changing phone_number and/or enable_whatsapp
                user.enable_whatsapp = enable_whatsapp
                user.phone_number = get_or_create_phone_number(phone_number)
                user.save()
                messages.add_message(request, messages.SUCCESS, MESSAGE_KEY__PHONE_NUMBER_UPDATE_SUCCESS)

                event_properties = {}
                if old_phone_number is not None:
                    event_properties['old phone number'] = old_phone_number
                event_properties['new phone number'] = user.phone_number.value()
                if old_enable_whatsapp is not None:
                    event_properties['old enable whatsapp'] = old_enable_whatsapp
                event_properties['new enable whatsapp'] = user.enable_whatsapp
            
                send_amplitude_event.delay(
                    'account - updated phone number',
                    user_uuid=user.uuid,
                    ip=get_ip_address(request),
                    event_properties=event_properties
                )
            else:
                messages.add_message(request, messages.SUCCESS, MESSAGE_KEY__PHONE_NUMBER_UPDATE_TRY_AGAIN)

            return HttpResponseRedirect(reverse('users:settings'))
    else:
        phone_number = request.GET.get('phone_number')

        p = get_or_create_phone_number(phone_number)
        send_whatsapp_code.send_whatsapp_code(user, whatsapp_purposes.UPDATE_PHONE_NUMBER, phone_number=p)
        form = forms.UpdatePhoneNumberForm(initial={
            'phone_number': phone_number,
            'enable_whatsapp': request.GET.get('enable_whatsapp') == 'True'
        }, **kwargs)

    return TemplateResponse(request, 'relationships/confirm_phone_number_change.html', {'form': form})

def log_out(request):
    logout(request)
    return _next_or_else_response(request.GET.get('next'), reverse('home'))

def user_detail(request, uuid):
    template_name = 'relationships/user_detail.html'
    return TemplateResponse(request, template_name, {})

def history(request):
    template_name = 'relationships/contacts.html'
    return TemplateResponse(request, template_name, {})

def requirements(request):
    template_name = 'relationships/status.html'
    return TemplateResponse(request, template_name, {})

def user_list(request):
    template_name = 'relationships/user_list.html'
    return TemplateResponse(request, template_name, {})

def suggestions(request, uuid):
    template_name = 'relationships/user_detail_suggestions.html'
    return TemplateResponse(request, template_name, {})

def lookup(request):
    template_name = 'relationships/lookup.html'
    return TemplateResponse(request, template_name, {})

def alert_list(request):
    template_name = 'relationships/alerts.html'
    return TemplateResponse(request, template_name, {})

def alert_detail(request, id):
    template_name = 'relationships/alert_detail.html'
    return TemplateResponse(request, template_name, {})

def alert_create(request):
    template_name = 'relationships/alert_create.html'
    return TemplateResponse(request, template_name, {})

def alert_edit(request):
    template_name = 'relationships/status.html'
    return TemplateResponse(request, template_name, {})

def alert_delete(request):
    template_name = 'relationships/status.html'
    return TemplateResponse(request, template_name, {})




# CONVERT THIS TO RELATIONSHIPS
# @login_required
# def redirect_contact_whatsapp(request, id):
#     if request.method == 'POST':
#         contact = models.Contact.objects.get(pk=id)
#         text = request.POST.get('whatsapp_body')
#         text = text if type(text) == str and text.strip() != 0 else None

#         models.ContactAction.objects.create(
#             contact=contact,
#             type='whatsapp',
#             body=text
#         )
        
#         user = request.user.user
#         identify_amplitude_user.delay(
#             user_id=user.uuid,
#             user_properties={'num whatsapped': user.num_whatsapped()}
#         )

#         send_amplitude_event.delay(
#             'qualification - whatsapped',
#             user_uuid=user.uuid,
#             ip=get_ip_address(request),
#             event_properties={'contact id': contact.lead.id}
#         )

#         url = get_whatsapp_url(contact.phone_number.country_code, contact.phone_number.national_number, text)
#         return HttpResponseRedirect(url)

#CONVERT TO RELATIONSHIPS
# def _set_whatsapp_bodies(params, contact):
#     params['default_whatsapp_body'] = render_to_string(
#         'leads/text/default_whatsapp_message_body.txt', {
#         'first_name': contact.first_name,
#         'last_name': contact.last_name,
#         'lead_body': contact.lead.body,
#         'contact_comments': contact.comments
#     }).replace('\n', '\\n') # Replace newline to newline symbols to be rendered in JS
#     params['default_whatsapp_body_rows'] = params['default_whatsapp_body'].count('\\n')+1

#     last_action = models.ContactAction.objects.filter(
#         contact=contact,
#         type='whatsapp'
#     ).order_by('-created').first()
    
#     if last_action is not None and last_action.body is not None and last_action.body.strip() != '':
#         params['last_whatsapp_body'] = last_action.body.replace('\r\n', '\\n')
#         params['last_whatsapp_body_rows'] = last_action.body.count('\r\n')+1
#     else:
#         params['last_whatsapp_body_rows'] = 2












# @login_required
# def disable_whatsapp(request):
#     user = request.user.user
#     user.enable_whatsapp = False
#     user.save()
#     return _next_or_else_response(request.GET.get('next'), reverse('users:settings'))

# @ratelimit(key='user_or_ip', rate='500/h', block=True, method=['GET'])
# def magic_login(request, uuid):
#     if uuid is not None:
#         dju = authenticate(uuid)
#         if dju is not None:
#             login(request, dju)

#     next_url = request.GET.get('next')
#     models.MagicLinkRedirect.objects.create(
#         uuid=uuid,
#         next=next_url
#     )

#     send_amplitude_event.delay(
#         'account - logged in',
#         user_uuid=uuid,
#         ip=get_ip_address(request),
#         event_properties={
#             'login type': 'magic',
#             'next': next_url
#         }
#     )
    
#     return _next_or_else_response(next_url, reverse('home'))

# def user_detail__following(request, uuid):
#     template_name = 'relationships/user_detail__following.html'
#     return TemplateResponse(request, template_name, {})

# def user_detail__followers(request, uuid):
#     template_name = 'relationships/user_detail__followers.html'
#     return TemplateResponse(request, template_name, {})

# def user_detail__contacted(request, uuid):
#     template_name = 'relationships/user_detail__contacted.html'
#     return TemplateResponse(request, template_name, {})

# def user_detail__reviews(request, uuid):
#     template_name = 'relationships/user_detail__reviews.html'
#     return TemplateResponse(request, template_name, {})

# def user_detail__friends(request, uuid):
#     template_name = 'relationships/user_detail__following.html'
#     return TemplateResponse(request, template_name, {})

# def friend_requests(request, uuid):
#     template_name = 'relationships/friend_requests.html'
#     return TemplateResponse(request, template_name, {})

# def confirm_email_login(request):
#     if request.user.is_authenticated:
#         return HttpResponseRedirect(reverse('home')) # Go home if authenticated

#     if request.method == 'POST':
#         form = forms.ConfirmEmailLoginForm(request.POST)
#         if form.is_valid():
#             user = form.user
#             use_email_code(user)
#             dju = authenticate(user.django_user.username) # Passwordless
#             if dju is not None:
#                 login(request, dju)
                
#                 send_amplitude_event.delay(
#                     'account - logged in',
#                     user_uuid=form.user.uuid,
#                     ip=get_ip_address(request),
#                     event_properties={
#                         'login type': 'email',
#                         'next': form.cleaned_data.get('next')
#                     }
#                 )

#                 cookie_uuid, _ = get_or_create_cookie_uuid(request)
#                 models.LoginAction.objects.create(
#                     user=user,
#                     cookie_uuid=cookie_uuid,
#                     type='email'
#                 )
#                 response = _next_or_else_response(form.cleaned_data.get('next'), reverse('home'))
#                 return set_cookie_uuid(response, cookie_uuid)

#     elif request.method == 'GET':
#         uuid = request.GET.get('uuid')
#         user = user_uuid_exists(uuid)
#         if user is None:
#             return HttpResponseRedirect(reverse('login')) # Unlikely error (e.g., bug or user temperage). Direct to login. No need for message.

#         form = forms.ConfirmEmailLoginForm(initial={
#             'uuid': uuid,
#             'next': request.GET.get('next'),
#             'email': user.email.email
#         })

#     return TemplateResponse(request, 'relationships/confirm_email_login.html', {'form': form})

# import pytz, phonenumbers, random, urllib
# from django.core.validators import validate_email
# from django.core.exceptions import ValidationError
# from chat.tasks._archive.send_welcome_message import send_welcome_message
# from chat.tasks.send_confirm_login import send_confirm_login

# def m(request, file_to_render):
#     template_name = 'relationships/superio/%s' % file_to_render
#     return TemplateResponse(request, template_name, {})

# def email_update(request):
#     params = {
#         # 'form': form,
#         'countries': commods.Country.objects.annotate(
#             num_users=Count('users_w_this_country')).order_by('-num_users')
#     }

#     template_name = 'relationships/metronic/settings.html'
#     return TemplateResponse(request, template_name, params)


# def confirm_email(request):
#     template_name = 'relationships/metronic/confirm_email.html'
#     return TemplateResponse(request, template_name, {})

# def _log_in(request):
#     # Do not allow user to access this page if he is authenticated.
#     if request.user.is_authenticated:
#         return HttpResponseRedirect(reverse('leads:lead_create'))

#     if request.method == 'POST':
#         form = forms.LoginForm(request.POST)
#         if form.is_valid():
#             url = reverse('confirm_login')

#             user = form.user

#             # Include next as GET parameter in the URL
#             next = form.cleaned_data.get('next')
#             has_next = False
#             if next is not None and next.strip() != '':
#                 url += f'?next={next}'
#                 has_next = True

#             if form.email is not None:
#                 # Generate code
#                 sgtz = pytz.timezone(settings.TIME_ZONE)
#                 now = datetime.now(tz=sgtz)
                
#                 user.email_login_code = random.randint(100000, 999999)
#                 user.email_login_code_generated = now
#                 user.save()

#                 if has_next and url.endswith(next):
#                     url += f'&method=email'
#                 else:
#                     url += f'?method=email'

#                 url += f'&user={user.uuid}'

#                 # Send confirmation code by email
#                 send_email.delay(
#                     render_to_string('relationships/email/confirm_login_subject.txt', {}),
#                     render_to_string('relationships/email/confirm_login.txt', {'code': user.email_login_code}),
#                     'friend@everybase.co',
#                     [form.email.email]
#                 )
#             elif form.phone_number is not None:
#                 # Generate code
#                 sgtz = pytz.timezone(settings.TIME_ZONE)
#                 now = datetime.now(tz=sgtz)
                
#                 user.whatsapp_login_code = random.randint(100000, 999999)
#                 user.whatsapp_login_code_generated = now
#                 user.save()

#                 if has_next and url.endswith(next):
#                     url += f'&method=whatsapp'
#                 else:
#                     url += f'?method=whatsapp'

#                 url += f'&user={user.uuid}'

#                 # Send confirmation code by WhatsApp
#                 send_confirm_login.delay(form.user.id)

#             return HttpResponseRedirect(url)
#     else:
#         form = forms.LoginForm()

#     params = {'form': form}

#     # Read 'next' URL from GET parameters to form input.
#     # We'll add it to the redirect URL when the user submits this form.
#     next = request.GET.get('next')
#     if next is not None:
#         params['next'] = next

#     template_name = 'relationships/superio/login.html'
#     return TemplateResponse(request, template_name, params)

# def confirm_login(request):
#     # Do not allow user to access this page if he is authenticated.
#     if request.user.is_authenticated:
#         return HttpResponseRedirect(reverse('leads:lead_create'))

#     params = {}

#     if request.method == 'POST':
#         form = forms.ConfirmLoginForm(request.POST)
#         if form.is_valid():
#             method = form.cleaned_data.get('method')

#             user_uuid = form.cleaned_data.get('user_uuid')
#             user = models.User.objects.get(uuid=user_uuid) # User should exist after form check

#             # Update login timestamp
#             sgtz = pytz.timezone(settings.TIME_ZONE)
#             now = datetime.now(sgtz)
#             if method == 'email':
#                 user.last_email_login = now
#             elif method == 'whatsapp':
#                 user.last_whatsapp_login = now
#             user.save()

#             # Authenticate with the Django user's username (which is the UUID key of the Everybase user) without password.
#             dj_user = authenticate(user.django_user.username)
#             if dj_user is not None:
#                 # Successfully authenticated
#                 login(request, dj_user)

#                 # Amplitude calls
#                 send_amplitude_event.delay(
#                     'account - logged in',
#                     user_uuid=user.uuid,
#                     ip=get_ip_address(request)
#                 )

#                 next = form.cleaned_data.get('next')
#                 if next is not None and next.strip() != '':
#                     return HttpResponseRedirect(next)
#                 else:
#                     return HttpResponseRedirect(reverse('leads:lead_create'))
#     elif request.method == 'GET':
#         user_uuid = request.GET.get('user')

#         try:
#             user = models.User.objects.get(uuid=user_uuid)
#         except models.User.DoesNotExist:
#             # Invalid user UUID, direct to login page
#             return HttpResponseRedirect(reverse('login'))

#         method = request.GET.get('method')

#         initial = {
#             'user_uuid': user_uuid,
#             'method': method,
#             'next': request.GET.get('next')
#         }
        
#         if user.email is not None:
#             initial['email'] = user.email.email

#         if user.phone_number is not None:
#             initial['country_code'] = user.phone_number.country_code
#             initial['national_number'] = user.phone_number.national_number

#         form = forms.ConfirmLoginForm(initial=initial)

#     # Pass GET parameters

#     params['form'] = form
#     template = 'relationships/superio/confirm_login.html'
#     return TemplateResponse(request, template, params)

# def _register(request):
#     # Do not allow user to access this page if he is authenticated.
#     if request.user.is_authenticated:
#         return HttpResponseRedirect(reverse('leads:lead_create'))

#     if request.method == 'POST':
#         form = forms.RegisterForm(request.POST)
#         if form.is_valid():
            
#             # Get or create a new email for this user
#             email_str = form.cleaned_data.get('email')
#             email = None
#             if email_str is not None:
#                 email, _ = models.Email.objects.get_or_create(email=email_str)

#             # Parse phone number
#             ph_str = str(form.cleaned_data.get('phone_number'))
#             phone_number = None
#             if ph_str is not None and ph_str.strip() != '':
#                 parsed_ph = phonenumbers.parse(ph_str, None)
#                 ph_cc = parsed_ph.country_code
#                 ph_nn = parsed_ph.national_number
#                 # Get or create new phone number for this user
#                 phone_number, _ = models.PhoneNumber.objects.get_or_create(
#                     country_code=ph_cc,
#                     national_number=ph_nn
#                 )

#             # Get country
#             country_key = form.cleaned_data.get('country')
#             country = commods.Country.objects.get(programmatic_key=country_key)

#             # Create an Everybase user
#             user = models.User.objects.create(
#                 email=email,
#                 phone_number=phone_number,
#                 country=country,
#                 first_name=form.cleaned_data.get('first_name'),
#                 last_name=form.cleaned_data.get('last_name')
#             )

#             # Create new Django user
#             django_user, _ = User.objects.get_or_create(username=user.uuid)
#             # django_user.set_password(password)
#             django_user.save()

#             # Update user profile
#             sgtz = pytz.timezone(settings.TIME_ZONE)
#             user.registered = datetime.now(sgtz)
#             user.django_user = django_user
#             user.save()

#             django_user = authenticate(request, username=django_user.username)
#             if django_user is not None:
#                 login(request, django_user)

#             # Email user if email is specified
#             if email is not None:
#                 send_email.delay(
#                     render_to_string('relationships/email/welcome_subject.txt', {}),
#                     render_to_string('relationships/email/welcome.txt', {}),
#                     'friend@everybase.co',
#                     [email.email]
#                 )

#             # WhatsApp user if phone number is specified
#             if phone_number is not None:
#                 send_welcome_message.delay(user.id)

#             # Amplitude call
#             send_amplitude_event.delay(
#                 'account - registered',
#                 user_uuid=user.uuid,
#                 ip=get_ip_address(request)
#             )

#             next = form.cleaned_data.get('next')
#             if next is not None and next.strip() != '':
#                 return HttpResponseRedirect(next)
#             else:
#                 return HttpResponseRedirect(reverse('leads:lead_create'))
#     else:
#         form = forms.RegisterForm()

#     params = {
#         'form': form,
#         'countries': commods.Country.objects.annotate(
#             num_users=Count('users_w_this_country')).order_by('-num_users')
#     }

#     # Read 'next' URL from GET parameters to form input. We'll add it to the
#     # redirect URL when the user submits this form.
#     next = request.GET.get('next')
#     if next is not None:
#         params['next'] = next

#     template_name = 'relationships/superio/register.html'
#     return TemplateResponse(request, template_name, params)

# @login_required
# def profile(request):
#     if request.method == 'POST':
#         kwargs = {'request': request}
        
#         user = request.user.user

#         kwargs['last_email'] = user.email.email if user.email else None
#         kwargs['last_phone_number'] = f'+{user.phone_number.country_code}{user.phone_number.national_number}' if user.phone_number else None

#         form = forms.ProfileForm(request.POST, **kwargs)

#         if form.is_valid():
#             last_email = form.last_email
#             last_phone_number = form.last_phone_number
            
#             email = form.cleaned_data.get('email')
#             phone_number = form.cleaned_data.get('phone_number')

#             need_logout = False

#             if email is None or email.strip() == '':
#                 user.email = None
#             elif last_email != email:
#                 # User has updated his email
#                 email, _ = models.Email.objects.get_or_create(email=email)
#                 user.email = email
#                 need_logout = True

#             if phone_number is None or str(phone_number).strip() == '':
#                 user.phone_number = None
#             elif last_phone_number != phone_number :
#                 # User has updated his phone number
#                 ph = get_or_create_phone_number(str(phone_number))

#                 user.phone_number = ph
#                 need_logout = True

#             country_str = form.cleaned_data.get('country')
#             country = commods.Country.objects.get(programmatic_key=country_str)

#             user.first_name = form.cleaned_data.get('first_name')
#             user.last_name = form.cleaned_data.get('last_name')
#             user.country = country
#             user.save()

#             idampusr_props = {'country': user.country.programmatic_key}
#             idampusr_props['country code'] = user.phone_number.country_code if user.phone_number is not None else ''

#             ampevt_props = {'country': user.country.programmatic_key}
#             ampevt_props['country code'] = user.phone_number.country_code if user.phone_number is not None else ''

#             identify_amplitude_user.delay(
#                 user_id=user.uuid,
#                 user_properties=idampusr_props
#             )
#             send_amplitude_event.delay(
#                 'account - updated profile',
#                 user_uuid=user.uuid,
#                 ip=get_ip_address(request),
#                 event_properties=ampevt_props
#             )

#             if need_logout:
#                 messages.add_message(request, messages.INFO, 'You have updated your email and/or phone number. Please log in again.')
#                 logout(request)
#                 return HttpResponseRedirect(reverse('login'))

#             messages.add_message(request, messages.INFO, 'Profile updated.')
#             return HttpResponseRedirect(reverse('users:profile'))
#     else:
#         user = request.user.user
#         initial = {}
#         kwargs = {'request': request}
        
#         if user.first_name:
#             initial['first_name'] = user.first_name
        
#         if user.last_name:
#             initial['last_name'] = user.last_name

#         kwargs['last_email'] = user.email.email if user.email else None
#         initial['email'] = kwargs['last_email']
        
#         kwargs['last_phone_number'] = f'+{user.phone_number.country_code}{user.phone_number.national_number}' if user.phone_number else None
#         initial['phone_number'] = kwargs['last_phone_number']

#         if user.country:
#             initial['country'] = user.country.programmatic_key
        
#         form = forms.ProfileForm(initial=initial, **kwargs)

#     countries = commods.Country.objects.annotate(
#         num_users=Count('users_w_this_country')).order_by('-num_users')

#     params = {
#         'countries': countries,
#         'form': form
#     }

#     return render(request, 'relationships/superio/profile.html', params)

# @login_required
# def change_password(request):
#     if request.method == 'POST':
#         form = forms.PasswordChangeForm(request.POST)
#         if form.is_valid():
#             u = request.user

#             password = form.cleaned_data.get('password')
#             u.set_password(password)
#             u.save()

#             # Reauthenticate with the Django user's username (which is the UUID key of the
#             # Everybase user) and the supplied password.
#             user = authenticate(request, username=u.username, password=password)
#             if user is not None:
#                 login(request, user)

#             if user is not None:
#                 # Success
#                 messages.add_message(request, messages.INFO, 'Password updated.')
#                 return HttpResponseRedirect(reverse('users:change_password'))
#     else:
#         form = forms.PasswordChangeForm()

#     params = {'form': form}
#     return render(request, 'relationships/superio/change_password.html', params)

# from django.core.paginator import Paginator
# from django.db.models import DateTimeField
# from django.db.models.expressions import RawSQL
# from django.db.models.functions import Trunc
# from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchVectorField
# from leads import models as lemods

# from django.http import JsonResponse
# from django.views.generic.list import ListView
# from datetime import timedelta
# from common.tasks.send_amplitude_event import send_amplitude_event
# from common.utilities.get_ip_address import get_ip_address
# from relationships.utilities.save_user_agent import save_user_agent
# from relationships.utilities.kill_login_tokens import kill_login_tokens
# from relationships.utilities.kill_register_tokens import kill_register_tokens
# from chat.tasks.send_register_message import send_register_message
# from chat.tasks.send_login_message import send_login_message

# from sentry_sdk import capture_message
# from ratelimit.decorators import ratelimit

# def get_countries():
#     return commods.Country.objects.annotate(
#         number_of_users=Count('users_w_this_country'))\
#             .order_by('-number_of_users')

# @login_required
# def whatsapp(request, slug):
#     if request.user.user.id == slug:
#         # Disallow WhatsApp to self
#         return HttpResponseRedirect(reverse('users:user_detail', args=(slug,)))

#     contactee = models.User.objects.get(slug_link=slug)

#     if request.method == 'POST':
#         form = forms.WhatsAppBodyForm(request.POST)
#         if form.is_valid():
#             body = form.cleaned_data.get('body')
#             contactor = request.user.user

#             lemods.WhatsAppMessageBody.objects.create(
#                 contactor=contactor,
#                 contactee=contactee,
#                 body=body
#             )
            
#             response = HttpResponse(status=302) # Temporary redirect
#             response['Location'] = get_whatsapp_url(
#                 contactee.phone_number.country_code,
#                 contactee.phone_number.national_number
#             )
#             response['Location'] += '?text=' + render_to_string(
#                 'chat/bodies/whatsapp_author.txt', {
#                     'contactee': contactee,
#                     'contactor': contactor,
#                     'body': body
#             }).replace('\n', '%0A').replace(' ', '%20')

#             return response
#     else:
#         form = forms.WhatsAppBodyForm()

#     params = {
#         'contactee': contactee,
#         'form': form
#     }

#     last_msg_body = lemods.WhatsAppMessageBody.objects.\
#         filter(contactor=request.user.user).\
#         order_by('-created').\
#         first()

#     if last_msg_body is not None:
#         params['last_msg_body'] = last_msg_body.body

#     return render(request, 'relationships/message.html', params)

# def user_detail_lead_list(request, slug):
#     user = models.User.objects.get(slug_link=slug)
#     leads = models.Lead.objects.filter(author=user)

#     params = {'detail_user': user}

#     # Paginate

#     leads_per_page = 12
#     paginator = Paginator(leads, leads_per_page)

#     page_number = request.GET.get('page')
    
#     page_obj = paginator.get_page(page_number)
#     params['page_obj'] = page_obj

#     return render(request, 'relationships/user_detail_lead_list.html', params)

# @login_required
# def user_edit(request, slug):
#     if request.user.user.slug_link != slug:
#         # Disallow user from editing another's profile
#         return HttpResponseRedirect(reverse('users:user_detail', args=(slug,)))

#     user = models.User.objects.get(slug_link=slug)

#     if request.method == 'POST':
#         form = forms.UserEditForm(request.POST)
#         if form.is_valid():
#             get = lambda k : form.cleaned_data.get(k)

#             user.first_name = get('first_name')
#             user.last_name = get('last_name')
#             user.goods_string = get('goods_string')
#             user.is_buyer = get('is_buyer')
#             user.is_seller = get('is_seller')
#             user.is_buy_agent = get('is_buy_agent')
#             user.is_sell_agent = get('is_sell_agent')
#             user.has_company = get('has_company')
#             user.company_name = get('company_name')
#             user.languages_string = get('languages_string')
#             user.refresh_slug()

#             user.save()

#             # Reference slug_link here, it may have been updated.
#             return HttpResponseRedirect(
#                 reverse('users:user_detail', args=(user.slug_link,)))
#     else:
#         form = forms.UserEditForm(initial={
#             'first_name': user.first_name,
#             'last_name': user.last_name,
#             'goods_string': user.goods_string,
#             'is_buyer': user.is_buyer,
#             'is_seller': user.is_seller,
#             'is_buy_agent': user.is_buy_agent,
#             'is_sell_agent': user.is_sell_agent,
#             'has_company': user.has_company,
#             'company_name': user.company_name,
#             'languages_string': user.languages_string,
#         })

#     return render(request, 'relationships/user_edit.html', {'form': form})

# class UserLeadListView(ListView):
#     template_name = 'relationships/user_detail_lead_list.html'
#     context_object_name = 'leads'
#     model = lemods.Lead
#     paginate_by = 8

#     def get_queryset(self, **kwargs):
#         return lemods.Lead.objects.filter(
#             author=models.User.objects.get(slug_link=self.kwargs['slug'])
#         ).order_by('-created')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = models.User.objects.get(slug_link=self.kwargs['slug'])
#         context['detail_user'] = user
#         return context

# def register(request):
#     if request.method == 'POST':
#         form = forms.RegisterForm(request.POST)
#         if form.is_valid():
#             # Part of the form check includes checking if the phone number and
#             # email belongs to a registered user. If so, is_valid() will return
#             # False.

#             # Parse phone number
#             ph_str = form.cleaned_data.get('whatsapp_phone_number')
#             parsed_ph = phonenumbers.parse(str(ph_str), None)
#             ph_cc = parsed_ph.country_code
#             ph_nn = parsed_ph.national_number

#             # Get or create new phone number for this user
#             whatsapp = models.PhoneNumberType.objects.get(
#                 programmatic_key='whatsapp'
#             )
#             phone_number, _ = \
#                 models.PhoneNumber.objects.get_or_create(
#                 country_code=ph_cc,
#                 national_number=ph_nn
#             )
#             phone_number.types.add(whatsapp)
#             phone_number.save()

#             # Get or create a new email for this user
#             email, _ = models.Email.objects.get_or_create(
#                 email=form.cleaned_data.get('email')
#             )

#             # Get country from user's WhatsApp phone number country code
#             try:
#                 country = commods.Country.objects.get(country_code=ph_cc)
#             except commods.Country.DoesNotExist:
#                 country = None

#             has_company = form.cleaned_data.get('has_company')
#             if has_company is None:
#                 has_company = False

#             # Create an Everybase user
#             user = models.User.objects.create(
#                 phone_number=phone_number,
#                 first_name=form.cleaned_data.get('first_name'),
#                 last_name=form.cleaned_data.get('last_name'),
#                 has_company=has_company,
#                 company_name=form.cleaned_data.get('company_name'),
#                 email=email,
#                 goods_string=form.cleaned_data.get('goods_string'),
#                 is_buyer=form.cleaned_data.get('is_buyer'),
#                 is_seller=form.cleaned_data.get('is_seller'),
#                 is_buy_agent=form.cleaned_data.get('is_buy_agent'),
#                 is_sell_agent=form.cleaned_data.get('is_sell_agent'),
#                 languages_string=form.cleaned_data.get('languages_string'),
#                 country=country
#             )

#             # Kill all tokens
#             kill_register_tokens(user)

#             # Create new token
#             models.RegisterToken.objects.create(user=user)

#             # Send message
#             send_register_message.delay(user.id)

#             # Amplitude call
#             send_amplitude_event.delay(
#                 'account - registered',
#                 user_uuid=user.uuid,
#                 ip=get_ip_address(request),
#                 event_properties={
#                     'country_code': user.phone_number.country_code,
#                     'country': '' if user.country is None else user.country.programmatic_key,
#                     'has_company': '' if user.has_company is None else user.has_company,
#                     'is_buyer': '' if user.is_buyer is None else user.is_buyer,
#                     'is_seller': '' if user.is_seller is None else user.is_seller,
#                     'is_sell_agent': '' if user.is_sell_agent is None else user.is_sell_agent,
#                     'is_buy_agent': '' if user.is_buy_agent is None else user.is_buy_agent
#                 }
#             )

#             # Append next URL
#             next_url = form.cleaned_data.get('next')
#             confirm_register = reverse('confirm_register',
#                 kwargs={'user_uuid': user.uuid})

#             if next_url is not None:
#                 confirm_register += f'?next={next_url}'

#             # TODO Amplitude
#             save_user_agent(request, user)

#             return HttpResponseRedirect(confirm_register)
#     else:
#         form = forms.RegisterForm()

#     params = {'form': form}

#     # Read 'next' URL from GET parameters to form input. We'll add it to the
#     # redirect URL when the user submits this form.
#     next = request.GET.get('next')
#     if next is not None:
#         params['next'] = next

#     return render(request, 'relationships/register.html', params)

# @ratelimit(key='user_or_ip', rate='10/h', block=True, method=['POST'])
# def confirm_register(request, user_uuid):
#     user = models.User.objects.get(uuid=user_uuid)

#     if request.method == 'POST':
#         # User request to resend message

#         # Kill all tokens
#         kill_register_tokens(user)

#         # Create new token
#         models.RegisterToken.objects.create(user=user)
        
#         # Send message
#         send_register_message.delay(user.id)

#         # If the user requested to resend the message, read next URL and
#         # redirect to self. Because we're not using a Django form, we need to
#         # manually read the next parameter from the HTML form, and render it
#         # back into the URL as a GET parameter. Django will then call this URL
#         # again and render the parameter back into the form.

#         confirm_register = reverse('confirm_register',
#             kwargs={'user_uuid': user.uuid})

#         next_url = request.POST.get('next')

#         if next_url is not None:
#             confirm_register += f'?next={next_url}'
        
#         return HttpResponseRedirect(confirm_register)
    
#     params = {
#         'user_uuid': user_uuid,
#         'country_code': user.phone_number.country_code,
#         'national_number': user.phone_number.national_number
#     }

#     next_url = request.GET.get('next')
#     if next_url is not None and len(next_url.strip()) > 0:
#         params['next'] = next_url
#     else:
#         params['next'] = reverse('home')

#     return render(request,
#         'relationships/confirm_register.html', params)

# def is_registered(request, user_uuid):
#     """This view is called in the background of the confirm_register page to
#     ascertain if the user has confirmed his registration by replying 'yes' to
#     the chatbot.
#     """
#     try:
#         # If the user has confirmed registration - i.e., replied 'yes' to the
#         # chatbot when sent a verification message, his Everybase User model
#         # will have an associated Django user model. Here, we check for the
#         # associated Django user model.

#         django_user = User.objects.get(username=user_uuid)
#     except User.DoesNotExist:
#         # User has not confirmed registration - i.e., no associated Django user
#         return JsonResponse({'r': False})

#     # Authenticate user
#     in_user = authenticate(django_user.username)
#     if in_user is not None:
#         # Authentication successful, log user in
#         login(request, in_user)

#         user = models.User.objects.get(uuid=user_uuid)

#         kill_register_tokens(user)

#         # TODO Amplitude
#     else:
#         capture_message('User not able to log in after registration. Django\
# user ID: %d, user ID: %d' % (django_user.id, django_user.user.id),
#         level='error')

#     return JsonResponse({'r': True})

# def log_in(request):
#     if request.method == 'POST':
#         form = forms.LoginForm(request.POST)
#         if form.is_valid():
#             # Parse phone number
#             ph_str = form.cleaned_data.get('whatsapp_phone_number')
#             parsed_ph = phonenumbers.parse(str(ph_str), None)
#             ph_cc = parsed_ph.country_code
#             ph_nn = parsed_ph.national_number

#             phone_number = models.PhoneNumber.objects.get(
#                 country_code=ph_cc,
#                 national_number=ph_nn
#             )

#             user = models.User.objects.filter(
#                 phone_number=phone_number.id, # User has phone number
#                 registered__isnull=False, # User is registered
#                 django_user__isnull=False # User has a Django user linked
#             ).first()
            
#             next_url = form.cleaned_data.get('next')

#             # Kill all tokens
#             kill_login_tokens(user)

#             # Create login token
#             models.LoginToken.objects.create(user=user)

#             # Send message
#             send_login_message.delay(user.id)

#             # Amplitude call
#             send_amplitude_event.delay(
#                 'account - logged in',
#                 user_uuid=user.uuid,
#                 ip=get_ip_address(request)
#             )

#             confirm_login_url = reverse('confirm_login',
#                 kwargs={'user_uuid': user.uuid})

#             if next_url is not None:
#                 confirm_login_url += f'?next={next_url}'

#             save_user_agent(request, user)
            
#             return HttpResponseRedirect(confirm_login_url)
#     else:
#         form = forms.LoginForm()

#     params = {'form': form}

#     # Read 'next' URL from GET parameters to form input. We'll add it to the
#     # redirect URL when the user submits this form.
#     next = request.GET.get('next')
#     if next is not None:
#         params['next'] = next

#     return render(request, 'relationships/login.html', params)

# @ratelimit(key='user_or_ip', rate='10/h', block=True, method=['POST'])
# def confirm_login(request, user_uuid):
#     if request.method == 'POST':
#         # Resend login message

#         # Note: we use the same LoginForm class as the log_in view.
#         form = forms.LoginForm(request.POST)
#         if form.is_valid():
#             # Parse phone number
#             ph_str = form.cleaned_data.get('whatsapp_phone_number')
#             parsed_ph = phonenumbers.parse(str(ph_str), None)
#             ph_cc = parsed_ph.country_code
#             ph_nn = parsed_ph.national_number

#             try:
#                 phone_number = models.PhoneNumber.objects.get(
#                     country_code=ph_cc,
#                     national_number=ph_nn
#                 )

#                 user = models.User.objects.filter(
#                     phone_number=phone_number.id, # User has phone number
#                     registered__isnull=False, # User is registered
#                     django_user__isnull=False # User has a Django user linked
#                 ).first()

#                 # Kill all tokens
#                 kill_login_tokens(user)

#                 # Create login token
#                 models.LoginToken.objects.create(user=user)

#                 # Create token and send message
#                 send_login_message.delay(user.id)

#                 return HttpResponseRedirect(
#                     reverse('confirm_login', kwargs={'user_uuid': user.uuid}))
                
#             except (models.User.DoesNotExist, models.PhoneNumber.DoesNotExist):
#                 # Not possible - unless user hacked the form
#                 return HttpResponseRedirect(reverse('login', kwargs={}))

#     user = models.User.objects.get(uuid=user_uuid)
#     params = {
#         'user_uuid': user_uuid,
#         'country_code': user.phone_number.country_code,
#         'national_number': user.phone_number.national_number,
#     }

#     # Read 'next' URL from GET parameters to be rendered as a form input. We'll
#     # add it to the redirect URL when the user submits this form.
#     next_url = request.GET.get('next')
#     if next_url is not None and len(next_url.strip()) > 0:
#         params['next'] = next_url
#     else:
#         params['next'] = reverse('home')

#     return render(request, 'relationships/confirm_login.html', params)

# def is_logged_in(request, user_uuid):
#     """This view is called in the background of the confirm_login page to
#     ascertain if the user has confirmed his login by replying 'yes' to the
#     chatbot.
#     """
#     user = models.User.objects.get(uuid=user_uuid)

#     # Get latest token for this user.
#     # Note: do not filter conditions here because the latest token for the
#     #   matching conditions may not be the latest-of-all token for this user.
#     token = models.LoginToken.objects.filter(user=user.id)\
#         .order_by('-created').first()
    
#     if token is not None:
#         expiry_datetime = token.created + timedelta(
#             seconds=settings.LOGIN_TOKEN_EXPIRY_SECS)
#         sgtz = pytz.timezone(settings.TIME_ZONE)
#         if datetime.now(tz=sgtz) < expiry_datetime and \
#             user.django_user is not None and token.activated is not None and \
#             token.is_not_latest is None:
#             # Checks passed
#             #   Token is not expired
#             #   User is registered (i.e., user.django_user is not None)
#             #   Token has been activated via chatbot (activated is not None)
#             #   Token is latest (is_not_latest is None)

#             django_user = user.django_user

#             # Authenticate user
#             in_user = authenticate(django_user.username)

#             if in_user is not None:
#                 # Authentication successful, log the user in with password
#                 login(request, in_user, backend=\
#                     'relationships.auth.backends.DirectBackend')

#                 # TODO Amplitude
#                 save_user_agent(request, user)

#                 return JsonResponse({'l': True})

#     return JsonResponse({'l': False})

# def log_out(request):
#     logout(request)
#     next_url = request.GET.get('next')
#     if next_url is not None:
#         return HttpResponseRedirect(next_url)

#     return HttpResponseRedirect(reverse('home'))

# @login_required
# @csrf_exempt
# def toggle_save_user(request, slug):
#     if request.user.user.slug_link == slug:
#         # Disallow saving of self
#         return HttpResponseRedirect(reverse('users:user_detail', args=(slug,)))

#     def toggle():
#         try:
#             saved_user = models.SavedUser.objects.get(
#                 savee=models.User.objects.get(slug_link=slug),
#                 saver=request.user.user
#             )

#             # Toggle save-unsave
#             saved_user.active = not saved_user.active
#             saved_user.save()
#         except models.SavedUser.DoesNotExist:
#             saved_user = models.SavedUser.objects.create(
#                 savee=models.User.objects.get(slug_link=slug),
#                 saver=request.user.user,
#                 active=True
#             )
        
#         return {'s': saved_user.active}

#     if request.method == 'POST':
#         # AJAX call, toggle save-unsave, return JSON.
#         return JsonResponse(toggle())

#     # Unauthenticated call. User will be given the URL to click only if the
#     # user is authenticated. Otherwise, a click on the 'update_profile' button will
#     # result in an AJAX post to this URL.
#     #
#     # Toggle save-unsave, redirect user to next URL.
#     toggle()

#     # Read 'next' URL from GET parameters. Redirect user there if the
#     # parameter exists. Other redirect user to default user details page.
#     next_url = request.GET.get('next')
#     if next_url is not None and len(next_url.strip()) > 0:
#         return HttpResponseRedirect(next_url)
#     else:
#         return HttpResponseRedirect(
#             reverse('users:user_detail', args=(slug,)))

# def user_list(request):
#     user = request.user.user if request.user.is_authenticated else None

#     get = lambda s : request.GET.get(s)

#     commented_only = get('commented_only')
#     saved_only = get('saved_only')
#     connected_only = get('connected_only')
#     first_name = get('first_name')    
#     last_name = get('last_name')
#     company_name = get('company_name')
#     country = get('country')
#     goods_string = get('goods_string')
#     languages = get('languages')
#     is_buy_agent = get('is_buy_agent')
#     buy_agent_details = get('buy_agent_details')
#     is_sell_agent = get('is_sell_agent')
#     sell_agent_details = get('sell_agent_details')
#     is_logistics_agent = get('is_logistics_agent')
#     logistics_agent_details = get('logistics_agent_details')

#     users = models.User.objects.all()

#     is_not_empty = lambda s : s is not None and s.strip() != ''
#     match = lambda t, v: is_not_empty(t) and t == v

#     if user is not None:
#         # Allow these options only if user is authenticated

#         if match(commented_only, 'on'):
#             # Commented only is checked
#             commentees = models.UserComment.objects.filter(
#                 commentor=user,
#                 deleted__isnull=True
#             ).values('commentee')

#             users = users.filter(id__in=commentees)
        
#         if match(saved_only, 'on'):
#             # Saved only is checked
#             savee = models.SavedUser.objects.filter(
#                 saver=user,
#                 deleted__isnull=True,
#                 active=True
#             ).values('savee')

#             users = users.filter(id__in=savee)

#         if match(connected_only, 'on'):
#             # Connected only is checked
#             connections = lemods.WhatsAppMessageBody.objects\
#                 .filter(contactee=user)\
#                 .values('contactor')
            
#             connections.union(lemods.WhatsAppMessageBody.objects\
#                 .filter(contactor=user)\
#                 .values('contactee'))

#             users = users.filter(id__in=connections)

#     order_by = [Trunc('created', 'month', output_field=DateTimeField()).desc()]

#     # First name
#     if is_not_empty(first_name):
#         # First name is filled
#         first_name_vec = SearchVector('first_name_vec')
#         first_name_qry = SearchQuery(first_name)
#         users = users.annotate(
#             first_name_vec=RawSQL('first_name_vec', [],
#                 output_field=SearchVectorField()))\
#             .annotate(first_name_rank=SearchRank(first_name_vec, first_name_qry))
        
#         order_by.append('-first_name_rank')

#     # Last name
#     if is_not_empty(last_name):
#         # Last name is filled
#         last_name_vec = SearchVector('last_name_vec')
#         last_name_qry = SearchQuery(last_name)
#         users = users.annotate(
#             last_name_vec=RawSQL('last_name_vec', [],
#                 output_field=SearchVectorField()))\
#             .annotate(last_name_rank=SearchRank(last_name_vec, last_name_qry))
        
#         order_by.append('-last_name_rank')

#     # Company name
#     if is_not_empty(company_name):
#         # Company name is filled
#         company_name_vec = SearchVector('company_name_vec')
#         company_name_qry = SearchQuery(company_name)
#         users = users.annotate(
#             company_name_vec=RawSQL('company_name_vec', [],
#                 output_field=SearchVectorField()))\
#             .annotate(company_name_rank=SearchRank(company_name_vec, company_name_qry))
        
#         order_by.append('-company_name_rank')

#     # Country
#     if is_not_empty(country) and country.strip() != 'any_country':
#         # Buy country is selected
#         c = commods.Country.objects.get(programmatic_key=country)
#         users = users.filter(country=c)

#     # Goods and services
#     if is_not_empty(goods_string):
#         # Company name is filled
#         goods_string_vec = SearchVector('goods_string_vec')
#         goods_string_qry = SearchQuery(goods_string)
#         users = users.annotate(
#             goods_string_vec=RawSQL('goods_string_vec', [],
#                 output_field=SearchVectorField()))\
#             .annotate(goods_string_rank=SearchRank(goods_string_vec, goods_string_qry))
        
#         order_by.append('-goods_string_rank')

#     # Languages
#     if is_not_empty(languages):
#         # Company name is filled
#         languages_string_vec = SearchVector('languages_string_vec')
#         languages_qry = SearchQuery(languages)
#         users = users.annotate(
#             languages_string_vec=RawSQL('languages_string_vec', [],
#                 output_field=SearchVectorField()))\
#             .annotate(languages_rank=SearchRank(languages_string_vec, languages_qry))
        
#         order_by.append('-languages_rank')

#     if match(is_buy_agent, 'on'):
#         # Is buy agent is checked
#         users = users.filter(is_buy_agent=True)

#         if is_not_empty(buy_agent_details):
#             # Buy agent details not empty
#             buy_agent_details_vec = SearchVector('buy_agent_details_vec')
#             buy_agent_details_qry = SearchQuery(buy_agent_details)
#             users = users.annotate(
#                 buy_agent_details_vec=RawSQL('buy_agent_details_vec', [],
#                     output_field=SearchVectorField()))\
#                 .annotate(buy_agent_details_rank=SearchRank(buy_agent_details_vec, buy_agent_details_qry))
            
#             order_by.append('-buy_agent_details_rank')

#     if match(is_sell_agent, 'on'):
#         # Is sell agent is checked
#         users = users.filter(is_sell_agent=True)

#         if is_not_empty(sell_agent_details):
#             # Sell agent details not empty
#             sell_agent_details_vec = SearchVector('sell_agent_details_vec')
#             sell_agent_details_qry = SearchQuery(sell_agent_details)
#             users = users.annotate(
#                 sell_agent_details_vec=RawSQL('sell_agent_details_vec', [],
#                     output_field=SearchVectorField()))\
#                 .annotate(sell_agent_details_rank=SearchRank(sell_agent_details_vec, sell_agent_details_qry))
            
#             order_by.append('-sell_agent_details_rank')

#     if match(is_logistics_agent, 'on'):
#         # Is logistics agent is checked
#         users = users.filter(is_logistics_agent=True)

#         if is_not_empty(sell_agent_details):
#             # Logistics agent details not empty
#             logistics_agent_details_vec = SearchVector('logistics_agent_details_vec')
#             logistics_agent_details_qry = SearchQuery(logistics_agent_details)
#             users = users.annotate(
#                 logistics_agent_details_vec=RawSQL('logistics_agent_details_vec', [],
#                     output_field=SearchVectorField()))\
#                 .annotate(logistics_agent_details_rank=SearchRank(logistics_agent_details_vec, logistics_agent_details_qry))
            
#             order_by.append('-logistics_agent_details_rank')

#     # Save lead query if it's not the default (empty) form post
#     # if is_not_empty(commented_only) or is_not_empty(saved_only) or\
#     #     is_not_empty(connected_only) or is_not_empty(first_name) or\
#     #     is_not_empty(last_name) or is_not_empty(company_name) or\
#     #     not match(country, 'any_country') or is_not_empty(goods_string) or\
#     #     is_not_empty(languages) or is_not_empty(is_buy_agent) or\
#     #     is_not_empty(buy_agent_details) or is_not_empty(is_sell_agent) or\
#     #     is_not_empty(sell_agent_details) or is_not_empty(is_logistics_agent) or\
#     #     is_not_empty(logistics_agent_details):
#         # models.UserQuery.objects.create(
#         #     user=user,
#         #     commented_only=commented_only,
#         #     saved_only=saved_only,
#         #     connected_only=connected_only,
#         #     first_name=first_name,
#         #     last_name=last_name,
#         #     company_name=company_name,
#         #     country=country,
#         #     goods_string=goods_string,
#         #     languages=languages,
#         #     is_buy_agent=is_buy_agent,
#         #     buy_agent_details=buy_agent_details,
#         #     is_sell_agent=is_sell_agent,
#         #     sell_agent_details=sell_agent_details,
#         #     is_logistics_agent=is_logistics_agent,
#         #     logistics_agent_details=logistics_agent_details
#         # )

#     # Set contact parameters

#     params = {}
#     params['countries'] = get_countries()
#     params['commented_only'] = commented_only
#     params['saved_only'] = saved_only
#     params['connected_only'] = connected_only
#     params['first_name'] = first_name
#     params['last_name'] = last_name
#     params['company_name'] = company_name
#     params['country'] = country
#     params['goods_string'] = goods_string
#     params['languages'] = languages
#     params['is_buy_agent'] = is_buy_agent
#     if match(is_buy_agent, 'on'):
#         params['buy_agent_details'] = buy_agent_details
#     params['is_sell_agent'] = is_sell_agent
#     if match(is_sell_agent, 'on'):
#         params['sell_agent_details'] = sell_agent_details
#     params['is_logistics_agent'] = is_logistics_agent
#     if match(is_logistics_agent, 'on'):
#         params['logistics_agent_details'] = logistics_agent_details

#     # Order users

#     users = users.order_by(*order_by)

#     # Paginate

#     users_per_page = 9
#     paginator = Paginator(users, users_per_page)

#     page_number = request.GET.get('page')
    
#     page_obj = paginator.get_page(page_number)
#     params['page_obj'] = page_obj

#     return render(request, 'relationships/user_list.html', params)