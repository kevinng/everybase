from datetime import datetime

from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages

from . import forms, models
from .tasks.send_register_token import send_register_token
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

            send_register_token.delay(token.token)

            return HttpResponseRedirect(
                reverse('relationships:verify_whatsapp_number',
                    kwargs={'token_str': token.token}))
    else:
        form = forms.RegisterForm()

    return render(request, 'relationships/register.html', {'form': form})

def verify_whatsapp_number(request, token_str):
    if request.method == 'POST':
        # Resend token via WhatsApp
        send_register_token.delay(token_str)
        return HttpResponseRedirect(
            reverse('relationships:verify_whatsapp_number',
                kwargs={'token_str': token_str}))

    token_obj = models.RegisterToken.objects.get(token=token_str)
    return render(request,
        'relationships/verify_whatsapp_number.html', {'token': token_obj})

def confirm_whatsapp_number(request, token_str):
    token_obj = models.RegisterToken.objects.get(token=token_str)
    user = token_obj.user

    # Create Django user
    django_user, du_is_new = User.objects.get_or_create(username=str(user.id))
    if du_is_new:
        # First time clicking the link - register

        # Set unusable password for Django user and save
        django_user.set_unusable_password()
        django_user.save()

        # Update user profile
        user.registered = datetime.now()
        user.django_user = django_user
        user.save()

        # Log the user in
        # Note: only works the first time this (register) link is used
        in_user = authenticate(django_user.username)
        if in_user is not None:
            # User authenticated by a backend successfully - login
            login(request, in_user)
        else:
            capture_message('User not able to log in after registration. \
Django user ID: %d, user ID: %d' % (django_user.id, user.id), level='error')

        messages.info(request, 'Welcome %s, your registration is complete.')

    return HttpResponseRedirect(reverse('leads__root:list'))

def login(request):
    template_name = 'relationships/login.html'
    return TemplateResponse(request, template_name, {})