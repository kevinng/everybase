from django import forms
from django.core.exceptions import ValidationError
from common.utilities.is_censored import is_censored
from . import models

from phonenumber_field.formfields import PhoneNumberField
import phonenumbers

_require_msg = 'This field is required.'
_censor_msg = 'Don\'t share contact details here. You may share contact details later.'

class UserEditForm(forms.Form):
    # Censorship applies
    first_name = forms.CharField(
        required=True,
        min_length=1,
        max_length=20
    )
    # Censorship applies
    last_name = forms.CharField(
        required=True,
        min_length=1,
        max_length=20
    )

    has_company = forms.BooleanField(
        required=False
    )
    # Censorship applies
    company_name = forms.CharField(
        required=False
    )

    # Censorship applies
    goods_string = forms.CharField(
        required=True,
        min_length=1,
        max_length=200
    )
    # Censorship applies
    languages_string = forms.CharField(
        required=True,
        min_length=1,
        max_length=200
    )

    # is_buy_agent = forms.BooleanField(required=False)
    # Censorship applies
    # buy_agent_details = forms.CharField(required=False)

    # is_sell_agent = forms.BooleanField(required=False)
    # Censorship applies
    # sell_agent_details = forms.CharField(required=False)

    # is_logistics_agent = forms.BooleanField(required=False)
    # Censorship applies
    # logistics_agent_details = forms.CharField(required=False)

    # Next URL after registration
    next = forms.CharField(required=False)

    def clean(self):
        super(UserEditForm, self).clean()

        has_error = False

        if is_censored(self.cleaned_data.get('first_name')):
            self.add_error('first_name', _censor_msg)
            has_error = True

        if is_censored(self.cleaned_data.get('last_name')):
            self.add_error('last_name', _censor_msg)
            has_error = True

        if self.cleaned_data.get('has_company'):
            company_name = self.cleaned_data.get('company_name')
            if company_name is None or company_name.strip() == '':
                self.add_error('company_name', _require_msg)
                has_error = True
            elif is_censored(self.cleaned_data.get('company_name')):
                self.add_error('company_name', _censor_msg)
                has_error = True

        if is_censored(self.cleaned_data.get('goods_string')):
            self.add_error('goods_string', _censor_msg)
            has_error = True

        if is_censored(self.cleaned_data.get('languages_string')):
            self.add_error('languages_string', _censor_msg)
            has_error = True

        # if self.cleaned_data.get('is_buy_agent'):
        #     buy_agent_details = self.cleaned_data.get('buy_agent_details')
        #     if buy_agent_details is None or buy_agent_details.strip() == '':
        #         self.add_error('buy_agent_details', _require_msg)
        #         has_error = True
        #     elif is_censored(buy_agent_details):
        #         self.add_error('buy_agent_details', _censor_msg)
        #         has_error = True

        # if self.cleaned_data.get('is_sell_agent'):
        #     sell_agent_details = self.cleaned_data.get('sell_agent_details')
        #     if sell_agent_details is None or sell_agent_details.strip() == '':
        #         self.add_error('sell_agent_details', _require_msg)
        #         has_error = True
        #     elif is_censored(sell_agent_details):
        #         self.add_error('sell_agent_details', _censor_msg)
        #         has_error = True

        # if self.cleaned_data.get('is_logistics_agent'):
        #     logistics_agent_details = self.cleaned_data.get('logistics_agent_details')
        #     if logistics_agent_details is None or logistics_agent_details.strip() == '':
        #         self.add_error('logistics_agent_details', _require_msg)
        #         has_error = True
        #     elif is_censored(logistics_agent_details):
        #         self.add_error('logistics_agent_details', _censor_msg)
        #         has_error = True

        if has_error:
            raise ValidationError(None)

        return self.cleaned_data

class RegisterForm(forms.Form):
    whatsapp_phone_number = PhoneNumberField(required=True)
    
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

    has_company = forms.BooleanField(required=False)

    # Validated only if has_company is checked.
    company_name = forms.CharField(required=False)
    
    email = forms.EmailField(
        required=True
    )

    goods_string = forms.CharField(
        required=True,
        min_length=1,
        max_length=200
    )

    # No validations, for survey only.
    is_buyer = forms.BooleanField(required=False)
    is_seller = forms.BooleanField(required=False)
    is_buy_agent = forms.BooleanField(required=False)
    is_sell_agent = forms.BooleanField(required=False)

    languages_string = forms.CharField(
        required=True,
        min_length=1,
        max_length=200
    )

    # Next URL after registration
    next = forms.CharField(required=False)

    def clean(self):
        super(RegisterForm, self).clean()

        has_error = False

        phone_number = self.cleaned_data.get('whatsapp_phone_number')
        if phone_number is not None:
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
                    self.add_error('whatsapp_phone_number', 'This phone number belongs to an existing user. Please ensure you\'ve entered your phone number correctly.')
                    has_error = True
            except models.PhoneNumber.DoesNotExist:
                # Good - no user has this phone number
                pass

        email = self.cleaned_data.get('email')

        if email is not None:
            try:
                email = models.Email.objects.get(email=email)

                user_w_email = models.User.objects.filter(
                    email=email.id, # User has email
                    registered__isnull=False, # User is registered
                    django_user__isnull=False # User has a Django user linked
                ).first()

                if user_w_email is not None:
                    self.add_error('email', 'This email belongs to an existing user. Please ensure you \'ve entered your email correctly.')
                    has_error = True
            except models.Email.DoesNotExist:
                # Good - no user has this email
                pass

        if self.cleaned_data.get('has_company'):
            company_name = self.cleaned_data.get('company_name')
            if company_name is None or company_name.strip() == '':
                self.add_error('company_name', _require_msg)
                has_error = True

        if has_error:
            raise ValidationError(None)

        return self.cleaned_data

class WhatsAppBodyForm(forms.Form):
    body = forms.CharField()

class LoginForm(forms.Form):
    whatsapp_phone_number = PhoneNumberField(required=True)
    next = forms.CharField(required=False)

    def clean(self):
        super(LoginForm, self).clean()

        # Parse phone number
        try:
            ph_str = self.cleaned_data.get('whatsapp_phone_number')
            parsed_ph = phonenumbers.parse(str(ph_str), None)
            ph_cc = parsed_ph.country_code
            ph_nn = parsed_ph.national_number
        except Exception as e:
            raise ValidationError(None)

        # Check existence of phone number
        try:
            phone_number = models.PhoneNumber.objects.get(
                country_code=ph_cc,
                national_number=ph_nn
            )
        except models.PhoneNumber.DoesNotExist:
            self.add_error('whatsapp_phone_number', "Account don't exist.")
            raise ValidationError(None)

        user = models.User.objects.filter(
            phone_number=phone_number.id, # User has phone number
            registered__isnull=False, # User is registered
            django_user__isnull=False # User has a Django user linked
        ).first()

        # Check existence of user
        if user is None:
            self.add_error('whatsapp_phone_number', "Account don't exist.")
            raise ValidationError(None)

        return self.cleaned_data

class UserCommentForm(forms.Form):
    comment_id = forms.IntegerField(required=False)
    body = forms.CharField()

    def clean(self):
        super(UserCommentForm, self).clean()
        body = self.cleaned_data.get('body')

        if is_censored(body):
            self.add_error('body', _censor_msg)
            raise ValidationError(None)

        return self.cleaned_data