from logging import exception
from django import forms
from django.core.exceptions import ValidationError

from . import models

from phonenumber_field.formfields import PhoneNumberField
import phonenumbers

class UserForm(forms.Form):
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
    
    email = forms.EmailField(
        required=True
    )

    has_company = forms.BooleanField(
        required=False
    )
    company_name = forms.CharField(
        required=False
    )

    goods_string = forms.CharField(
        required=True,
        min_length=1,
        max_length=200
    )
    languages_string = forms.CharField(
        required=True,
        min_length=1,
        max_length=200
    )

    is_buy_agent = forms.BooleanField(required=False)
    buy_agent_details = forms.CharField(required=False)

    is_sell_agent = forms.BooleanField(required=False)
    sell_agent_details = forms.CharField(required=False)

    is_logistics_agent = forms.BooleanField(required=False)
    logistics_agent_details = forms.CharField(required=False)

    # Next URL after registration
    next = forms.CharField(required=False)

    def clean(self):
        super(UserForm, self).clean()

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

        require_msg = 'This field is required.'
        
        if self.cleaned_data.get('has_company'):
            company_name = self.cleaned_data.get('company_name')
            if company_name is None or company_name.strip() == '':
                self.add_error('company_name', require_msg)
                has_error = True

        if self.cleaned_data.get('is_buy_agent'):
            buy_agent_details = self.cleaned_data.get('buy_agent_details')
            if buy_agent_details is None or buy_agent_details.strip() == '':
                self.add_error('buy_agent_details', require_msg)
                has_error = True

        if self.cleaned_data.get('is_sell_agent'):
            sell_agent_details = self.cleaned_data.get('sell_agent_details')
            if sell_agent_details is None or sell_agent_details.strip() == '':
                self.add_error('sell_agent_details', require_msg)
                has_error = True

        if self.cleaned_data.get('is_logistics_agent'):
            logistics_agent_details = self.cleaned_data.get('logistics_agent_details')
            if logistics_agent_details is None or logistics_agent_details.strip() == '':
                self.add_error('logistics_agent_details', require_msg)
                has_error = True

        if has_error:
            raise ValidationError(None)

        return self.cleaned_data

class UserEditForm(forms.Form):
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
    goods_string = forms.CharField(
        required=True,
        min_length=1,
        max_length=200
    )
    languages_string = forms.CharField(
        required=True,
        min_length=1,
        max_length=200
    )
    is_not_agent = forms.BooleanField(
        required=False
    )

class WhatsAppBodyForm(forms.Form):
    body = forms.CharField()

class CommentForm(forms.Form):
    body = forms.CharField()
    is_public = forms.BooleanField(required=False)

# class RegisterForm(forms.Form):
#     whatsapp_phone_number = PhoneNumberField(required=True)
    
#     first_name = forms.CharField(
#         required=True,
#         min_length=1,
#         max_length=20
#     )
#     last_name = forms.CharField(
#         required=True,
#         min_length=1,
#         max_length=20
#     )
    
#     email = forms.EmailField(
#         required=True
#     )

#     has_company = forms.BooleanField(
#         required=False
#     )
#     company_name = forms.CharField(
#         required=False
#     )

#     goods_string = forms.CharField(
#         required=True,
#         min_length=1,
#         max_length=200
#     )
#     languages_string = forms.CharField(
#         required=True,
#         min_length=1,
#         max_length=200
#     )

#     is_buy_agent = forms.BooleanField(required=False)
#     buy_agent_details = forms.CharField(required=False)

#     is_sell_agent = forms.BooleanField(required=False)
#     sell_agent_details = forms.CharField(required=False)

#     is_logistics_agent = forms.BooleanField(required=False)
#     logistics_agent_details = forms.CharField(required=False)

#     # Next URL after registration
#     next = forms.CharField(required=False)

#     def clean(self):
#         super(RegisterForm, self).clean()

#         has_error = False

#         phone_number = self.cleaned_data.get('whatsapp_phone_number')
#         if phone_number is not None:
#             parsed_ph = phonenumbers.parse(str(phone_number), None)
#             ph_cc = parsed_ph.country_code
#             ph_nn = parsed_ph.national_number

#             try:
#                 phone_number = models.PhoneNumber.objects.get(
#                     country_code=ph_cc,
#                     national_number=ph_nn
#                 )

#                 user_w_ph = models.User.objects.filter(
#                     phone_number=phone_number.id, # User has phone number
#                     registered__isnull=False, # User is registered
#                     django_user__isnull=False # User has a Django user linked
#                 ).first()

#                 if user_w_ph is not None:
#                     self.add_error('whatsapp_phone_number', 'This phone number belongs to an existing user. Please ensure you\'ve entered your phone number correctly.')
#                     has_error = True
#             except models.PhoneNumber.DoesNotExist:
#                 # Good - no user has this phone number
#                 pass

#         email = self.cleaned_data.get('email')

#         if email is not None:
#             try:
#                 email = models.Email.objects.get(email=email)

#                 user_w_email = models.User.objects.filter(
#                     email=email.id, # User has email
#                     registered__isnull=False, # User is registered
#                     django_user__isnull=False # User has a Django user linked
#                 ).first()

#                 if user_w_email is not None:
#                     self.add_error('email', 'This email belongs to an existing user. Please ensure you \'ve entered your email correctly.')
#                     has_error = True
#             except models.Email.DoesNotExist:
#                 # Good - no user has this email
#                 pass
        
#         if self.cleaned_data.get('has_company'):
#             company_name = self.cleaned_data.get('company_name')
#             if company_name is None or company_name.strip() == '':
#                 self.add_error('company_name', 'This field is required.')
#                 has_error = True

#         if self.cleaned_data.get('is_buy_agent'):
#             buy_agent_details = self.cleaned_data.get('buy_agent_details')
#             if buy_agent_details is None or buy_agent_details.strip() == '':
#                 self.add_error('buy_agent_details', 'This field is required.')
#                 has_error = True

#         if self.cleaned_data.get('is_sell_agent'):
#             sell_agent_details = self.cleaned_data.get('sell_agent_details')
#             if sell_agent_details is None or sell_agent_details.strip() == '':
#                 self.add_error('sell_agent_details', 'This field is required.')
#                 has_error = True

#         if self.cleaned_data.get('is_logistics_agent'):
#             logistics_agent_details = self.cleaned_data.get('logistics_agent_details')
#             if logistics_agent_details is None or logistics_agent_details.strip() == '':
#                 self.add_error('logistics_agent_details', 'This field is required.')
#                 has_error = True

#         if has_error:
#             raise ValidationError(None)

#         return self.cleaned_data

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