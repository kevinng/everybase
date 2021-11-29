from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from everybase import settings
from . import forms, models

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

            # TODO: we need to set the user's country also

            # Create user
            user = models.User.objects.create(
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
                languages_string=form.cleaned_data.get('languages'),
                phone_number=phone_number,
                email=email
            )

            # Create register token
            token = models.RegisterToken.objects.create(user=user)

            # TODO
            # send_register_token.delay(token.token)

            return HttpResponseRedirect(
                reverse('relationships:register_link',
                    kwargs={'token_str': token.token}))
    else:
        form = forms.RegisterForm()

    return render(request, 'relationships/register.html', {'form': form})

def register_link(request, token_str):
    token = models.RegisterToken.objects.get(token=token_str)
    if request.method == 'POST':
        
        # Get current timezone
        sgtz = pytz.timezone(settings.TIME_ZONE)
        token.refreshed = datetime.now(tz=sgtz)

        # TODO:
        # Resend token via WhatsApp
        # send_register_token.delay(token_str)
        
        return HttpResponseRedirect(
            reverse('relationships:register_link',
                kwargs={'token_str': token_str}))

    return render(request,
        'relationships/register_link.html', {'token': token})





# TODO this link is not in used
def confirm_register(request, token_str):
    token_obj = models.RegisterToken.objects.get(token=token_str)
    user = token_obj.user

    expiry_datetime = token_obj.created + timedelta(
        seconds=settings.REGISTER_TOKEN_EXPIRY_SECS)
    sgtz = pytz.timezone(settings.TIME_ZONE)
    if datetime.now(tz=sgtz) < expiry_datetime:
        # ##### Token has not expired
        
        # Create Django user
        django_user, du_is_new = User.objects.get_or_create(
            username=str(user.id))
        if du_is_new:
            # Register user - only works once

            # Set unusable password for Django user and save
            django_user.set_unusable_password()
            django_user.save()

            # Update user profile
            user.registered = datetime.now(sgtz)
            user.django_user = django_user
            user.save()

            # Update token activated timestamp
            token_obj.activated = datetime.now(sgtz)
            token_obj.save()

        # Log the user in - will keep working until token is expired
        in_user = authenticate(django_user.username)
        if in_user is not None:
            # User authenticated by a backend successfully - login
            login(request, in_user)
        else:
            capture_message('User not able to log in after registration. \
    Django user ID: %d, user ID: %d' % (django_user.id, user.id), level='error')

        messages.info(request, 'Welcome %s, your registration is complete.' % in_user.user.first_name)

    else:
        # ##### Token has expired
        messages.info(request, 'This registration link has expired.')

    return HttpResponseRedirect(reverse('leads__root:list'))











def log_in(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            # Send login link

            # Parse phone number
            ph_str = form.cleaned_data.get('whatsapp_phone_number')
            parsed_ph = phonenumbers.parse(str(ph_str), None)
            ph_cc = parsed_ph.country_code
            ph_nn = parsed_ph.national_number

            # Get user with this phone number
            phone_number = models.PhoneNumber.objects.get(
                country_code=ph_cc,
                national_number=ph_nn
            )
            user_w_ph = models.User.objects.filter(
                phone_number=phone_number.id, # User has phone number
                registered__isnull=False, # User is registered
                django_user__isnull=False # User has a Django user linked
            ).first()

            # Create login token
            token = models.LoginToken.objects.create(user=user_w_ph)

            send_login_token.delay(token.token)

            return HttpResponseRedirect(
                reverse('relationships:login_link',
                    kwargs={'token_str': token.token}))
    else:
        form = forms.LoginForm()

    return render(request, 'relationships/login.html', {'form': form})

def log_in_link(request, token_str):
    token = models.LoginToken.objects.get(token=token_str)
    if request.method == 'POST':
        
        # Get current timezone
        sgtz = pytz.timezone(settings.TIME_ZONE)
        token.refreshed = datetime.now(tz=sgtz)

        # Resend token via WhatsApp
        send_login_token.delay(token_str)
        
        return HttpResponseRedirect(
            reverse('relationships:login_link',
                kwargs={'token_str': token_str}))

    return render(request,
        'relationships/login_link.html', {'token': token})

def confirm_log_in(request, token_str):
    token = models.LoginToken.objects.get(token=token_str)
    user = token.user

    expiry_datetime = token.created + timedelta(
        seconds=settings.LOGIN_TOKEN_EXPIRY_SECS)
    sgtz = pytz.timezone(settings.TIME_ZONE)
    if datetime.now(tz=sgtz) < expiry_datetime:
        # ##### Token has not expired

        # Update token activated timestamp
        token.activated = datetime.now(sgtz)
        token.save()

        # Authenticate the user
        django_user = token.user.django_user
        user = authenticate(django_user.username)
        if user is not None:
            # User authenticated by a backend successfully - login
            login(request, user)
        else:
            capture_message('User not able to log in with token. \
    Django user ID: %d, user ID: %d' % (django_user.id, user.id), level='error')

        messages.info(request, 'Welcome %s.' % user.user.first_name)

    else:
        # ##### Token has expired
        messages.info(request, 'This login link has expired.')

    return HttpResponseRedirect(reverse('leads__root:list'))

def log_out(request):
    logout(request)
    messages.info(request, 'You\'ve logged out.')
    return HttpResponseRedirect(reverse('leads__root:list'))

def log_in_if_registered(request, token_str):
    try:
        token = models.RegisterToken.objects.get(token=token_str)
    except:
        return HttpResponse(status=404)
    
    if token.activated is not None:
        # This token has been activated

        # Authenticate the user
        user = authenticate(token.user.django_user.username)
        if user is not None:
            # User authenticated by a backend successfully - login
            login(request, user)
            messages.info(request, 'Welcome %s.' % user.user.first_name)
            return JsonResponse({'logged_in': True})

    return JsonResponse({'logged_in': False})

def log_in_if_logged_in(request, token_str):
    try:
        token = models.LoginToken.objects.get(token=token_str)
    except:
        return HttpResponse(status=404)
    
    if token.activated is not None:
        # This token has been activated

        # Authenticate the user
        user = authenticate(token.user.django_user.username)
        if user is not None:
            # User authenticated by a backend successfully - login
            login(request, user)
            messages.info(request, 'Welcome %s.' % user.user.first_name)
            return JsonResponse({'logged_in': True})

    return JsonResponse({'logged_in': False})