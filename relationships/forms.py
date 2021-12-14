from django import forms
from django.core.exceptions import ValidationError
from django.db.models.fields import CharField

from . import models

from phonenumber_field.formfields import PhoneNumberField
import phonenumbers

class RegisterForm(forms.Form):
    whatsapp_phone_number = PhoneNumberField(
        required=True
    )
    first_name = forms.CharField(
        required=True,
        min_length=1,
        max_length=20
    )
    last_name = forms.CharField(
        required=True,
        min_length=1,
        max_length=20
    )
    email = forms.EmailField(
        required=True
    )
    languages_string = forms.CharField(
        required=True,
        min_length=1,
        max_length=200
    )
    # Errors associated with these fields are saved under 'i_am_a'.
    is_direct_buyer = forms.BooleanField(required=False)
    is_direct_seller = forms.BooleanField(required=False)
    is_buying_agent = forms.BooleanField(required=False)
    is_selling_agent = forms.BooleanField(required=False)
    next = forms.CharField(required=False)

    def clean(self):
        super(RegisterForm, self).clean()

        has_error = False

        # ##### Phone number should not already exist #####

        phone_number = self.cleaned_data.get('whatsapp_phone_number')

        # Phone number didn't pass field-level validation
        if phone_number is None:
            return self.cleaned_data

        parsed_ph = phonenumbers.parse(str(phone_number), None)
        ph_cc = parsed_ph.country_code
        ph_nn = parsed_ph.national_number

        try:
            phone_number = models.PhoneNumber.objects.get(
                country_code=ph_cc,
                national_number=ph_nn
            )

            user_w_ph = models.User.objects.filter(
                phone_number=phone_number.id, # User has phone number
                registered__isnull=False, # User is registered
                django_user__isnull=False # User has a Django user linked
            ).first()

            if user_w_ph is not None:
                self.add_error('whatsapp_phone_number', 'This phone number \
already exists. Please ensure you\'ve entered your phone number correctly.')
                has_error = True
        except models.PhoneNumber.DoesNotExist:
            # Good - no user has this phone number
            pass

        # ##### Email should not already exist for a registered user

        email = self.cleaned_data.get('email')

        if email is None:
            # Email didn't pass field-level validation
            return self.cleaned_data

        try:
            email = models.Email.objects.get(email=email)

            user_w_email = models.User.objects.filter(
                email=email.id, # User has email
                registered__isnull=False, # User is registered
                django_user__isnull=False # User has a Django user linked
            ).first()

            if user_w_email is not None:
                self.add_error('email', 'This email is in use. Please ensure \
you \'ve entered your email correctly.')
                has_error = True
        except models.Email.DoesNotExist:
            # Good - no user has this email
            pass

        # ##### At least 1 'I am a' option should be selected

        a = self.cleaned_data.get('is_direct_buyer')
        b = self.cleaned_data.get('is_direct_seller')
        c = self.cleaned_data.get('is_buying_agent')
        d = self.cleaned_data.get('is_selling_agent')

        if a is False and b is False and c is False and d is False:
            self.add_error(None, 'Please indicate if you\'re a buyer/seller, \
direct/agent.')
            has_error = True

        if has_error:
            raise ValidationError(None)

        return self.cleaned_data

class VerifyWhatsAppNumberForm(forms.Form):
    whatsapp_phone_number = PhoneNumberField(required=True)

class LoginForm(forms.Form):
    whatsapp_phone_number = PhoneNumberField(required=True)
    next = forms.CharField(required=False)