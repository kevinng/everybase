import pytz, phonenumbers, random
from datetime import datetime

from chat.tasks.send_welcome_message import send_welcome_message
from chat.tasks.send_confirm_login import send_confirm_login

from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Count
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
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

# Named 'log_in' and not 'login' to prevent clash with Django login
def log_in(request):
    # Direct user to home if he's already logged in
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = form.user
            sgtz = pytz.timezone(settings.TIME_ZONE)
            now = datetime.now(tz=sgtz)

            if form.email is not None:
                # Generate code
                user.email_login_code = random.randint(100000, 999999)
                user.email_login_code_generated = now
                user.save()

                url = reverse('confirm_email_login')

                # Send confirmation code by email
                send_email.delay(
                    render_to_string('relationships/email/confirm_login_subject.txt', {}),
                    render_to_string('relationships/email/confirm_login.txt', {'code': user.email_login_code}),
                    'friend@everybase.co',
                    [form.email.email]
                )
            elif form.phone_number is not None:
                # Generate code
                user.whatsapp_login_code = random.randint(100000, 999999)
                user.whatsapp_login_code_generated = now
                user.save()

                url = reverse('confirm_whatsapp_login')

                # Send confirmation code by WhatsApp
                send_confirm_login.delay(form.user.id)

            url += f'?uuid={user.uuid}'

            # Include next as GET parameter in the URL
            next = form.cleaned_data.get('next')
            if next is not None and next.strip() != '':
                url += f'&next={next}'

            return HttpResponseRedirect(url)
    else:
        form = forms.LoginForm()

    params = {'form': form}

    # Read 'next' URL from GET parameters to form input - we'll add it to the redirect URL when the user submits the form the next time.
    next = request.GET.get('next')
    if next is not None:
        params['next'] = next

    template_name = 'relationships/metronic/login.html'
    return TemplateResponse(request, template_name, params)

def confirm_email_login(request):
    # Direct user to home if he's already logged in
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'POST':
        form = forms.ConfirmEmailLoginForm(request.POST)

        if form.is_valid():
            # Update login timestamp
            sgtz = pytz.timezone(settings.TIME_ZONE)
            now = datetime.now(sgtz)
            form.user.last_email_login = now

            # Authenticate with the Django user's username (i.e., Everybase user UUID) without password
            dj_user = authenticate(form.user.django_user.username)
            if dj_user is not None:
                # Successfully authenticated
                login(request, dj_user)

                # Amplitude calls
                send_amplitude_event.delay(
                    'account - logged in',
                    user_uuid=form.user.uuid,
                    ip=get_ip_address(request)
                )

                next = form.cleaned_data.get('next')
                if next is not None and next.strip() != '':
                    return HttpResponseRedirect(next)
                else:
                    return HttpResponseRedirect(reverse('home'))

    elif request.method == 'GET':
        uuid = request.GET.get('uuid')

        try:
            user = models.User.objects.get(uuid=uuid)
        except models.User.DoesNotExist:
            # Invalid user UUID, direct to login page
            return HttpResponseRedirect(reverse('login'))

        initial = {
            'uuid': uuid,
            'next': request.GET.get('next'),
            'email': user.email.email
        }

        form = forms.ConfirmEmailLoginForm(initial=initial)

    template = 'relationships/metronic/confirm_email_login.html'
    return TemplateResponse(request, template, {'form': form})

def confirm_whatsapp_login(request):
    # Direct user to home if he's already logged in
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    
    if request.method == 'POST':
        form = forms.ConfirmWhatsAppLoginForm(request.POST)

        if form.is_valid():
            # Update login timestamp
            sgtz = pytz.timezone(settings.TIME_ZONE)
            now = datetime.now(sgtz)
            form.user.last_email_login = now

            # Authenticate with the Django user's username (i.e., Everybase user UUID) without password
            dj_user = authenticate(form.user.django_user.username)
            if dj_user is not None:
                # Successfully authenticated
                login(request, dj_user)

                # Amplitude calls
                send_amplitude_event.delay(
                    'account - logged in',
                    user_uuid=form.user.uuid,
                    ip=get_ip_address(request)
                )

                next = form.cleaned_data.get('next')
                if next is not None and next.strip() != '':
                    return HttpResponseRedirect(next)
                else:
                    return HttpResponseRedirect(reverse('home'))

    elif request.method == 'GET':
        uuid = request.GET.get('uuid')

        try:
            user = models.User.objects.get(uuid=uuid)
        except models.User.DoesNotExist:
            # Invalid user UUID, direct to login page
            return HttpResponseRedirect(reverse('login'))

        initial = {
            'uuid': uuid,
            'next': request.GET.get('next'),
            'phone_number': f'{user.phone_number.country_code} {user.phone_number.national_number}'
        }

        form = forms.ConfirmWhatsAppLoginForm(initial=initial)
    
    template = 'relationships/metronic/confirm_whatsapp_login.html'
    return TemplateResponse(request, template, {'form': form})





















def magic_login(request, uuid):
    # Logs in the user 'magically'
    if uuid is not None:
        dj_user = authenticate(uuid)
        if dj_user is not None:
            # Successfully authenticated
            login(request, dj_user)

    next = request.GET.get('next')
    if next is not None and next.strip() != '':
        return HttpResponseRedirect(next)
    else:
        return HttpResponseRedirect(reverse('leads:lead_create'))

def confirm_email(request):
    template_name = 'relationships/metronic/confirm_email.html'
    return TemplateResponse(request, template_name, {})



def _log_in(request):
    # Do not allow user to access this page if he is authenticated.
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('leads:lead_create'))

    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            url = reverse('confirm_login')

            user = form.user

            # Include next as GET parameter in the URL
            next = form.cleaned_data.get('next')
            has_next = False
            if next is not None and next.strip() != '':
                url += f'?next={next}'
                has_next = True

            if form.email is not None:
                # Generate code
                sgtz = pytz.timezone(settings.TIME_ZONE)
                now = datetime.now(tz=sgtz)
                
                user.email_login_code = random.randint(100000, 999999)
                user.email_login_code_generated = now
                user.save()

                if has_next and url.endswith(next):
                    url += f'&method=email'
                else:
                    url += f'?method=email'

                url += f'&user={user.uuid}'

                # Send confirmation code by email
                send_email.delay(
                    render_to_string('relationships/email/confirm_login_subject.txt', {}),
                    render_to_string('relationships/email/confirm_login.txt', {'code': user.email_login_code}),
                    'friend@everybase.co',
                    [form.email.email]
                )
            elif form.phone_number is not None:
                # Generate code
                sgtz = pytz.timezone(settings.TIME_ZONE)
                now = datetime.now(tz=sgtz)
                
                user.whatsapp_login_code = random.randint(100000, 999999)
                user.whatsapp_login_code_generated = now
                user.save()

                if has_next and url.endswith(next):
                    url += f'&method=whatsapp'
                else:
                    url += f'?method=whatsapp'

                url += f'&user={user.uuid}'

                # Send confirmation code by WhatsApp
                send_confirm_login.delay(form.user.id)

            return HttpResponseRedirect(url)
    else:
        form = forms.LoginForm()

    params = {'form': form}

    # Read 'next' URL from GET parameters to form input.
    # We'll add it to the redirect URL when the user submits this form.
    next = request.GET.get('next')
    if next is not None:
        params['next'] = next

    template_name = 'relationships/superio/login.html'
    return TemplateResponse(request, template_name, params)














def confirm_login(request):
    # Do not allow user to access this page if he is authenticated.
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('leads:lead_create'))

    params = {}

    if request.method == 'POST':
        form = forms.ConfirmLoginForm(request.POST)
        if form.is_valid():
            method = form.cleaned_data.get('method')

            user_uuid = form.cleaned_data.get('user_uuid')
            user = models.User.objects.get(uuid=user_uuid) # User should exist after form check

            # Update login timestamp
            sgtz = pytz.timezone(settings.TIME_ZONE)
            now = datetime.now(sgtz)
            if method == 'email':
                user.last_email_login = now
            elif method == 'whatsapp':
                user.last_whatsapp_login = now
            user.save()

            # Authenticate with the Django user's username (which is the UUID key of the Everybase user) without password.
            dj_user = authenticate(user.django_user.username)
            if dj_user is not None:
                # Successfully authenticated
                login(request, dj_user)

                # Amplitude calls
                send_amplitude_event.delay(
                    'account - logged in',
                    user_uuid=user.uuid,
                    ip=get_ip_address(request)
                )

                next = form.cleaned_data.get('next')
                if next is not None and next.strip() != '':
                    return HttpResponseRedirect(next)
                else:
                    return HttpResponseRedirect(reverse('leads:lead_create'))
    elif request.method == 'GET':
        user_uuid = request.GET.get('user')

        try:
            user = models.User.objects.get(uuid=user_uuid)
        except models.User.DoesNotExist:
            # Invalid user UUID, direct to login page
            return HttpResponseRedirect(reverse('login'))

        method = request.GET.get('method')

        initial = {
            'user_uuid': user_uuid,
            'method': method,
            'next': request.GET.get('next')
        }
        
        if user.email is not None:
            initial['email'] = user.email.email

        if user.phone_number is not None:
            initial['country_code'] = user.phone_number.country_code
            initial['national_number'] = user.phone_number.national_number

        form = forms.ConfirmLoginForm(initial=initial)

    # Pass GET parameters

    params['form'] = form
    template = 'relationships/superio/confirm_login.html'
    return TemplateResponse(request, template, params)

def confirm_phone(request):
    template = 'relationships/metronic/confirm_phone.html'
    return TemplateResponse(request, template, {})

def register(request):
    template = 'relationships/metronic/register.html'
    return TemplateResponse(request, template, {})

def _register(request):
    # Do not allow user to access this page if he is authenticated.
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('leads:lead_create'))

    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            
            # Get or create a new email for this user
            email_str = form.cleaned_data.get('email')
            email = None
            if email_str is not None:
                email, _ = models.Email.objects.get_or_create(email=email_str)

            # Parse phone number
            ph_str = str(form.cleaned_data.get('phone_number'))
            phone_number = None
            if ph_str is not None and ph_str.strip() != '':
                parsed_ph = phonenumbers.parse(ph_str, None)
                ph_cc = parsed_ph.country_code
                ph_nn = parsed_ph.national_number
                # Get or create new phone number for this user
                phone_number, _ = models.PhoneNumber.objects.get_or_create(
                    country_code=ph_cc,
                    national_number=ph_nn
                )

            # Get country
            country_key = form.cleaned_data.get('country')
            country = commods.Country.objects.get(programmatic_key=country_key)

            # Create an Everybase user
            user = models.User.objects.create(
                email=email,
                phone_number=phone_number,
                country=country,
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name')
            )

            # Create new Django user
            django_user, _ = User.objects.get_or_create(username=user.uuid)
            # django_user.set_password(password)
            django_user.save()

            # Update user profile
            sgtz = pytz.timezone(settings.TIME_ZONE)
            user.registered = datetime.now(sgtz)
            user.django_user = django_user
            user.save()

            django_user = authenticate(request, username=django_user.username)
            if django_user is not None:
                login(request, django_user)

            # Email user if email is specified
            if email is not None:
                send_email.delay(
                    render_to_string('relationships/email/welcome_subject.txt', {}),
                    render_to_string('relationships/email/welcome.txt', {}),
                    'friend@everybase.co',
                    [email.email]
                )

            # WhatsApp user if phone number is specified
            if phone_number is not None:
                send_welcome_message.delay(user.id)

            # Amplitude call
            send_amplitude_event.delay(
                'account - registered',
                user_uuid=user.uuid,
                ip=get_ip_address(request)
            )

            next = form.cleaned_data.get('next')
            if next is not None and next.strip() != '':
                return HttpResponseRedirect(next)
            else:
                return HttpResponseRedirect(reverse('leads:lead_create'))
    else:
        form = forms.RegisterForm()

    params = {
        'form': form,
        'countries': commods.Country.objects.annotate(
            num_leads=Count('leads_buy_country')).order_by('-num_leads')
    }

    # Read 'next' URL from GET parameters to form input. We'll add it to the
    # redirect URL when the user submits this form.
    next = request.GET.get('next')
    if next is not None:
        params['next'] = next

    template_name = 'relationships/superio/register.html'
    return TemplateResponse(request, template_name, params)

def log_out(request):
    logout(request)
    next_url = request.GET.get('next')
    if next_url is not None:
        return HttpResponseRedirect(next_url)

    return HttpResponseRedirect(reverse('home'))

# Don't name it 'settings', it conflicts with 
def profile_settings(request):
    template_name = 'relationships/metronic/settings.html'
    return TemplateResponse(request, template_name, {})

@login_required
def profile(request):
    if request.method == 'POST':
        kwargs = {'request': request}
        
        user = request.user.user

        kwargs['last_email'] = user.email.email if user.email else None
        kwargs['last_phone_number'] = f'+{user.phone_number.country_code}{user.phone_number.national_number}' if user.phone_number else None

        form = forms.ProfileForm(request.POST, **kwargs)

        if form.is_valid():
            last_email = form.last_email
            last_phone_number = form.last_phone_number
            
            email = form.cleaned_data.get('email')
            phone_number = form.cleaned_data.get('phone_number')

            need_logout = False

            if email is None or email.strip() == '':
                user.email = None
            elif last_email != email:
                # User has updated his email
                email, _ = models.Email.objects.get_or_create(email=email)
                user.email = email
                need_logout = True

            if phone_number is None or str(phone_number).strip() == '':
                user.phone_number = None
            elif last_phone_number != phone_number :
                # User has updated his phone number
                parsed_ph = phonenumbers.parse(str(phone_number), None)
                ph_cc = parsed_ph.country_code
                ph_nn = parsed_ph.national_number

                ph, _ = models.PhoneNumber.objects.get_or_create(
                    country_code=ph_cc,
                    national_number=ph_nn
                )

                user.phone_number = ph
                need_logout = True

            country_str = form.cleaned_data.get('country')
            country = commods.Country.objects.get(programmatic_key=country_str)

            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.country = country
            user.save()

            idampusr_props = {'country': user.country.programmatic_key}
            idampusr_props['country code'] = user.phone_number.country_code if user.phone_number is not None else ''

            ampevt_props = {'country': user.country.programmatic_key}
            ampevt_props['country code'] = user.phone_number.country_code if user.phone_number is not None else ''

            identify_amplitude_user.delay(
                user_id=user.uuid,
                user_properties=idampusr_props
            )
            send_amplitude_event.delay(
                'account - updated profile',
                user_uuid=user.uuid,
                ip=get_ip_address(request),
                event_properties=ampevt_props
            )

            if need_logout:
                messages.add_message(request, messages.INFO, 'You have updated your email and/or phone number. Please log in again.')
                logout(request)
                return HttpResponseRedirect(reverse('login'))

            messages.add_message(request, messages.INFO, 'Profile updated.')
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        user = request.user.user
        initial = {}
        kwargs = {'request': request}
        
        if user.first_name:
            initial['first_name'] = user.first_name
        
        if user.last_name:
            initial['last_name'] = user.last_name

        kwargs['last_email'] = user.email.email if user.email else None
        initial['email'] = kwargs['last_email']
        
        kwargs['last_phone_number'] = f'+{user.phone_number.country_code}{user.phone_number.national_number}' if user.phone_number else None
        initial['phone_number'] = kwargs['last_phone_number']

        if user.country:
            initial['country'] = user.country.programmatic_key
        
        form = forms.ProfileForm(initial=initial, **kwargs)

    countries = commods.Country.objects.annotate(
        num_leads=Count('leads_buy_country')).order_by('-num_leads')

    params = {
        'countries': countries,
        'form': form
    }

    return render(request, 'relationships/superio/profile.html', params)

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


def m(request, file_to_render):
    template_name = 'relationships/superio/%s' % file_to_render
    return TemplateResponse(request, template_name, {})




























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
#             response['Location'] = get_non_tracking_whatsapp_link(
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
#     # user is authenticated. Otherwise, a click on the 'save' button will
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