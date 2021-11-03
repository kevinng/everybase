from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.shortcuts import render
from django.urls import reverse

from . import forms, models

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

            # TODO: send register token to user

            return HttpResponseRedirect(
                reverse('relationships:verify_whatsapp_number', args=()))
    else:
        form = forms.RegisterForm()

    return render(request, 'relationships/register.html', {'form': form})

def verify_whatsapp_number(request):
    return render(request, 'relationships/verify_whatsapp_number.html', {})

def login(request):
    template_name = 'relationships/login.html'
    return TemplateResponse(request, template_name, {})