import pytz
from datetime import datetime, timedelta

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.response import TemplateResponse

from everybase import settings
from common import models as commods
from relationships import forms, models
from relationships.utilities.save_user_agent import save_user_agent
from chat.tasks.send_register_link import send_register_link
from chat.tasks.send_login_link import send_login_link

from sentry_sdk import capture_message
import phonenumbers

def user_comments(request, pk):
    template_name = 'relationships/user_detail_comment_list.html'
    context = {}

    if request.method == 'POST':
        pass
    else:
        pass


    return TemplateResponse(request, template_name, context)

def user_leads(request, pk):
    template_name = 'relationships/user_detail_lead_list.html'
    context = {}
    return TemplateResponse(request, template_name, context)

def register(request):
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            # Part of the form check includes checking if the phone number and
            # email belongs to a REGISTERED user. If so, is_valid() will return
            # False.

            # Parse phone number
            ph_str = form.cleaned_data.get('whatsapp_phone_number')
            parsed_ph = phonenumbers.parse(str(ph_str), None)
            ph_cc = parsed_ph.country_code
            ph_nn = parsed_ph.national_number

            # Get or create new phone number for this user
            whatsapp = models.PhoneNumberType.objects.get(
                programmatic_key='whatsapp'
            )
            phone_number, _ = \
                models.PhoneNumber.objects.get_or_create(
                country_code=ph_cc,
                national_number=ph_nn
            )
            phone_number.types.add(whatsapp)
            phone_number.save()

            # Get or create a new email for this user
            email, _ = models.Email.objects.get_or_create(
                email=form.cleaned_data.get('email')
            )

            # Get country from user's WhatsApp phone number country code
            try:
                country = commods.Country.objects.get(country_code=ph_cc)
            except commods.Country.DoesNotExist:
                country = None

            # Get or create an Everybase user
            user, _ = models.User.objects.get_or_create(
                phone_number=phone_number)
            

            is_not_agent = form.cleaned_data.get('is_not_agent')
            if is_not_agent is None:
                is_not_agent = False

            # Override or set user details
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.languages_string = form.cleaned_data.get('languages')
            user.is_agent = not is_not_agent
            user.phone_number = phone_number
            user.email = email
            user.country = country
            user.save()

            # Send register link
            send_register_link.delay(user.id)

            # Append next URL
            next_url = form.cleaned_data.get('next')
            register_link = reverse('relationships:register_link',
                kwargs={'user_uuid': user.uuid})

            if next_url is not None:
                register_link += f'?next={next_url}'

            save_user_agent(request, user)

            return HttpResponseRedirect(register_link)
    else:
        form = forms.RegisterForm()

    params = {'form': form}

    # Read 'next' URL from GET parameters to form input. We'll add it to the
    # redirect URL when the user submits this form.
    next = request.GET.get('next')
    if next is not None:
        params['next'] = next

    return render(request, 'relationships/register.html', params)

def register_link(request, user_uuid):
    try:
        user = models.User.objects.get(uuid=user_uuid)
    except models.User.DoesNotExist:
        user = None

    if request.method == 'POST':
        # Resend message
        
        send_register_link.delay(user.id)

        # Read next URL and redirect to self, if the user requested to resend
        # the message. Because we're not using a Django form, we need to
        # manually read the next parameter from the HTML form, and render it
        # back into the URL as a GET parameter. Django will then call this URL
        # again and render the parameter back into the form.

        register_link = reverse('relationships:register_link',
            kwargs={'user_uuid': user.uuid})

        next_url = request.POST.get('next')

        if next_url is not None:
            register_link += f'?next={next_url}'
        
        return HttpResponseRedirect(register_link)
    
    params = {
        'user_uuid': user_uuid,
        'country_code': user.phone_number.country_code,
        'national_number': user.phone_number.national_number
    }

    next_url = request.GET.get('next')
    if next_url is not None and len(next_url.strip()) > 0:
        params['next'] = next_url
    else:
        params['next'] = reverse('leads__root:agents')

    return render(request,
        'relationships/register_link.html', params)

def confirm_register(request, user_uuid):
    try:
        django_user = User.objects.get(username=user_uuid)

        # Authenticate user
        in_user = authenticate(django_user.username)
        if in_user is not None:
            # Authentication successful, log user in
            login(request, in_user)
        else:
            capture_message('User not able to log in after registration. Django\
user ID: %d, user ID: %d' % (django_user.id, django_user.user.id), 
            level='error')

        messages.info(request, 'Welcome %s, your registration is complete.' % \
            django_user.user.first_name)
        
        return JsonResponse({'logged_in': True})
    except User.DoesNotExist:
        pass # User has not confirmed registration

    return JsonResponse({'logged_in': False})

def log_in(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            # Parse phone number
            ph_str = form.cleaned_data.get('whatsapp_phone_number')
            parsed_ph = phonenumbers.parse(str(ph_str), None)
            ph_cc = parsed_ph.country_code
            ph_nn = parsed_ph.national_number

            try:
                phone_number = models.PhoneNumber.objects.get(
                    country_code=ph_cc,
                    national_number=ph_nn
                )

                user = models.User.objects.filter(
                    phone_number=phone_number.id, # User has phone number
                    registered__isnull=False, # User is registered
                    django_user__isnull=False # User has a Django user linked
                ).first()

                next_url = form.cleaned_data.get('next')

                # If there is an activated, unexpired login token, log the user
                # in immediately without requiring the user to request for
                # another token.

                token = models.LoginToken.objects.filter(
                    user=user.id,
                    activated__isnull=False # Token is activated
                ).order_by('-created').first()

                if token is not None:
                    expiry_datetime = token.created + timedelta(
                        seconds=settings.LOGIN_TOKEN_EXPIRY_SECS)
                    sgtz = pytz.timezone(settings.TIME_ZONE)
                    if datetime.now(tz=sgtz) < expiry_datetime and \
                        user.django_user is not None and \
                        token.activated is not None:
                        # Token not expired, user is registered, token is 
                        # activated - log the user in immediately without
                        # requesting for another token.

                        # Log the user in.
                        django_user = user.django_user
                        in_user = authenticate(django_user.username)
                        if in_user is not None:
                            # Authentication successful, log the user in
                            login(request, in_user, backend=\
                                'relationships.auth.backends.DirectBackend')

                        if next_url is not None and next_url.strip() != '':
                            return HttpResponseRedirect(next_url)
                        
                        return HttpResponseRedirect(
                            reverse('leads__root:agents'))

                send_login_link.delay(user.id)

                login_link_url = reverse('relationships:login_link',
                    kwargs={'user_uuid': user.uuid})

                if next_url is not None:
                    login_link_url += f'?next={next_url}'

                save_user_agent(request, user)
                
                return HttpResponseRedirect(login_link_url)
            except (models.User.DoesNotExist, models.PhoneNumber.DoesNotExist):
                messages.info(request, 'Account not found. Create a new \
account.')
    else:
        form = forms.LoginForm()

    params = {'form': form}

    # Read 'next' URL from GET parameters to form input. We'll add it to the
    # redirect URL when the user submits this form.
    next = request.GET.get('next')
    if next is not None:
        params['next'] = next

    return render(request, 'relationships/login.html', params)

def log_in_link(request, user_uuid):
    user = models.User.objects.get(uuid=user_uuid)

    if request.method == 'POST':
        # Resend message

        # Note: we use the same LoginForm class as the log_in view.
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            # Parse phone number
            ph_str = form.cleaned_data.get('whatsapp_phone_number')
            parsed_ph = phonenumbers.parse(str(ph_str), None)
            ph_cc = parsed_ph.country_code
            ph_nn = parsed_ph.national_number

            try:
                phone_number = models.PhoneNumber.objects.get(
                    country_code=ph_cc,
                    national_number=ph_nn
                )

                user = models.User.objects.filter(
                    phone_number=phone_number.id, # User has phone number
                    registered__isnull=False, # User is registered
                    django_user__isnull=False # User has a Django user linked
                ).first()

                send_login_link.delay(user.id)

                return HttpResponseRedirect(
                    reverse('relationships:login_link',
                        kwargs={'user_uuid': user.uuid}))
                
            except (models.User.DoesNotExist, models.PhoneNumber.DoesNotExist):
                pass # Not possible
    
    params = {
        'user_uuid': user_uuid,
        'country_code': user.phone_number.country_code,
        'national_number': user.phone_number.national_number,
    }

    # Read 'next' URL from GET parameters to form input. We'll add it to the
    # redirect URL when the user submits this form.
    next_url = request.GET.get('next')
    if next_url is not None and len(next_url.strip()) > 0:
        params['next'] = next_url
    else:
        params['next'] = reverse('leads__root:agents')

    return render(request, 'relationships/login_link.html', params)

def confirm_log_in(request, user_uuid):
    """This view is polled by the login_link template periodically to check
    if the user has successfully logged in. If so - log the user in."""

    user = models.User.objects.get(uuid=user_uuid)

    token = models.LoginToken.objects.filter(
        user=user.id,
        activated__isnull=False # Token is activated
    ).order_by('-created').first()
    
    if token is not None:
        expiry_datetime = token.created + timedelta(
            seconds=settings.LOGIN_TOKEN_EXPIRY_SECS)
        sgtz = pytz.timezone(settings.TIME_ZONE)
        if datetime.now(tz=sgtz) < expiry_datetime and \
            user.django_user is not None and \
            token.activated is not None:
            # Token not expired, user is registered, token is activated - log
            # the user in.

            django_user = user.django_user

            # Authenticate user
            in_user = authenticate(django_user.username)
            if in_user is not None:
                # Authentication successful, log the user in
                login(request, in_user, backend=\
                    'relationships.auth.backends.DirectBackend')
                return JsonResponse({'logged_in': True})

    return JsonResponse({'logged_in': False})

def log_out(request):
    logout(request)
    messages.info(request, 'You\'ve logged out.')
    return HttpResponseRedirect(reverse('leads__root:agents'))