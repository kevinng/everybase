from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from everybase import settings
from common import models as commods
from relationships import forms, models
from chat.tasks.send_register_confirm import send_register_confirm
from chat.tasks.send_login_confirm import send_login_confirm

import pytz
from datetime import datetime, timedelta
from sentry_sdk import capture_message
import phonenumbers

def register(request):
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
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

            try:
                country = commods.Country.objects.get(country_code=ph_cc)
            except commods.Country.DoesNotExist:
                country = None

            # Create user
            user = models.User.objects.create(
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
                languages_string=form.cleaned_data.get('languages'),
                phone_number=phone_number,
                email=email,
                country=country
            )

            # Create/send register confirmation
            send_register_confirm.delay(user.id)

            return HttpResponseRedirect(
                reverse('relationships:register_link',
                    kwargs={'user_uuid': user.uuid}))
    else:
        form = forms.RegisterForm()

    return render(request, 'relationships/register.html', {'form': form})

def register_link(request, user_uuid):
    try:
        user = models.User.objects.get(uuid=user_uuid)
    except models.User.DoesNotExist:
        user = None

    if request.method == 'POST':

        # Resend token via WhatsApp
        send_register_confirm.delay(user.id)
        
        return HttpResponseRedirect(
            reverse('relationships:register_link',
                kwargs={'user_uuid': user_uuid}))

    return render(request,
        'relationships/register_link.html', {
            'user_uuid': user_uuid,
            'country_code': user.phone_number.country_code,
            'national_number': user.phone_number.national_number
        })

def confirm_register(request, user_uuid):
    # Create Django user
    django_user, du_is_new = User.objects.get_or_create(username=user_uuid)

    # Get Everybase user
    if du_is_new:
        # Set unusable password for Django user and save
        django_user.set_unusable_password()
        django_user.save()

        # Update user profile
        sgtz = pytz.timezone(settings.TIME_ZONE)
        user = models.User.objects.get(uuid=user_uuid)
        user.registered = datetime.now(sgtz)
        user.django_user = django_user
        user.save()

    if django_user is not None:
        # Authenticate user
        in_user = authenticate(django_user.username)
        if in_user is not None:
            # Authentication successful, log user in
            login(request, in_user)
        else:
            capture_message('User not able to log in after registration. Django\
    user ID: %d, user ID: %d' % (django_user.id, user.id), level='error')

        messages.info(request, 'Welcome %s, your registration is complete.' % \
            in_user.user.first_name)
        
        return JsonResponse({'logged_in': True})

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

                send_login_confirm.delay(user.id)

                return HttpResponseRedirect(
                    reverse('relationships:login_link',
                        kwargs={'user_uuid': user.uuid}))
            except (models.User.DoesNotExist, models.PhoneNumber.DoesNotExist):
                messages.info(request, 'Account not found. Create a new \
account.')
    else:
        form = forms.LoginForm()

    return render(request, 'relationships/login.html', {'form': form})

def log_in_link(request, user_uuid):
    user = models.User.objects.get(uuid=user_uuid)

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

                send_login_confirm.delay(user.id)

                return HttpResponseRedirect(
                    reverse('relationships:login_link',
                        kwargs={'user_uuid': user.uuid}))
            except (models.User.DoesNotExist, models.PhoneNumber.DoesNotExist):
                pass # Not possible

    return render(request,
        'relationships/login_link.html', {
            'user_uuid': user_uuid,
            'country_code': user.phone_number.country_code,
            'national_number': user.phone_number.national_number
        })

def confirm_log_in(request, user_uuid):
    user = models.User.objects.get(uuid=user_uuid)

    # Only the latest token is used
    token = models.LoginToken.objects.filter(
        user=user.id,
        activated__isnull=False # Token is activated
    ).order_by('-created').first()
    
    if token:
        expiry_datetime = token.created + timedelta(
            seconds=settings.LOGIN_TOKEN_EXPIRY_SECS)
        sgtz = pytz.timezone(settings.TIME_ZONE)
        if datetime.now(tz=sgtz) < expiry_datetime:
            # Token has not expired, log the user in
            django_user = user.django_user
            # Authenticate user
            in_user = authenticate(django_user.username)
            if in_user is not None:
                # Authentication successful, log user in
                login(request, in_user, backend=\
                    'relationships.auth.backends.DirectBackend')
                return JsonResponse({'logged_in': True})

    return JsonResponse({'logged_in': False})

def log_out(request):
    logout(request)
    messages.info(request, 'You\'ve logged out.')
    return HttpResponseRedirect(reverse('leads__root:list'))