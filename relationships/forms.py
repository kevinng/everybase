import phonenumbers, pytz, datetime
from phonenumber_field.formfields import PhoneNumberField

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from everybase import settings

from common import models as commods
from relationships import models

class ConfirmLoginForm(forms.Form):
    code = forms.CharField()
    method = forms.CharField()
    user_uuid = forms.CharField()
    next = forms.CharField(required=False)
    email = forms.CharField()
    country_code = forms.CharField()
    national_number = forms.CharField()

    def clean(self):
        super(ConfirmLoginForm, self).clean()

        code = self.cleaned_data.get('code')
        method = self.cleaned_data.get('method')
        user_uuid = self.cleaned_data.get('user_uuid')

        try:
            user = models.User.objects.get(uuid=user_uuid)
        except models.User.DoesNotExist:
            # Invalid user UUID, just tell the user code has expired.
            self.add_error('code', 'An error has occurred. Please request for another code.')
            raise ValidationError(None)

        if (method == 'email' and user.email_login_code != code) or\
            (method == 'whatsapp' and user.whatsapp_login_code != code):
            # Invalid code, just tell the user code has expired.
            self.add_error('code', 'Wrong code. Please try again.')
            raise ValidationError(None)

        # Check if code has expired

        if method == 'email':
            generated = user.email_login_code_generated
        elif method == 'whatsapp':
            generated = user.whatsapp_login_code_generated

        sgtz = pytz.timezone(settings.TIME_ZONE)
        now = datetime.datetime.now(tz=sgtz)
        difference = (now - generated).total_seconds()

        if difference > int(settings.LOGIN_CODE_EXPIRY_SECONDS):
            # Code has expired
            self.add_error('code', 'Code has expired. Please request for another code.')
            raise ValidationError(None)

        # Check if code has been used

        if method == 'email' and user.last_email_login is not None and user.email_login_code_generated is not None:
            if user.last_email_login > user.email_login_code_generated:
                self.add_error('code', 'Please request for another code.')
                raise ValidationError(None)
        elif method == 'whatsapp' and user.last_whatsapp_login is not None and user.whatsapp_login_code_generated is not None:
            if user.last_whatsapp_login > user.whatsapp_login_code_generated:
                self.add_error('code', 'Please request for another code.')
                raise ValidationError(None)

class LoginForm(forms.Form):
    email_or_phone_number = forms.CharField()
    next = forms.CharField(required=False)

    def clean(self):
        super(LoginForm, self).clean()

        self.email = None
        self.phone_number = None

        eph_str = self.cleaned_data.get('email_or_phone_number')

        # Check if string is an email address
        is_email = False
        try:
            validate_email(eph_str)
        except ValidationError as e:
            pass
        else:
            is_email = True

        # Check if string is a phone number
        is_phone_number = False
        try:
            ph = phonenumbers.parse(eph_str)
            is_phone_number = phonenumbers.is_valid_number(ph)
        except phonenumbers.phonenumberutil.NumberParseException:
            is_phone_number = False

        has_error = False
        if not is_email and not is_phone_number:
            self.add_error('email_or_phone_number', 'Enter valid email or phone number.')
            has_error = True
        
        if not has_error:
            # No error so far, check if account exists

            if is_email:
                # Valid email, check if an account exists

                try:
                    self.email = models.Email.objects.get(email=eph_str)
                    self.user = models.User.objects.filter(
                            email=self.email.id, # User has email
                            registered__isnull=False, # User is registered
                            django_user__isnull=False # User has a Django user linked
                        ).first()
                        
                    if self.user is None:
                        self.add_error('email_or_phone_number', 'Account does not exist.')
                        has_error = True

                except models.Email.DoesNotExist:
                    self.add_error('email_or_phone_number', 'Account does not exist.')
                    has_error = True

            elif is_phone_number:
                # Valid phone number, check if account exists

                try:
                    self.phone_number = models.PhoneNumber.objects.get(
                        country_code=ph.country_code,
                        national_number=ph.national_number
                    )
                    self.user = models.User.objects.filter(
                            phone_number=self.phone_number.id, # User has phone number
                            registered__isnull=False, # User is registered
                            django_user__isnull=False # User has a Django user linked
                        ).first()
                    
                    if self.user is None:
                        self.add_error('email_or_phone_number', 'Account does not exist.')
                        has_error = True
                except models.PhoneNumber.DoesNotExist:
                    self.add_error('email_or_phone_number', 'Account does not exist.')
                    has_error = True

        if has_error:
            raise ValidationError(None)

class RegisterForm(forms.Form):
    email = forms.EmailField(required=False)
    phone_number = PhoneNumberField(required=False)
    first_name = forms.CharField(
        min_length=1,
        max_length=20
    )
    last_name = forms.CharField(
        min_length=1,
        max_length=20
    )
    country = forms.CharField()

    # Next destination after user has registered
    next = forms.CharField(required=False)

    def clean(self):
        super(RegisterForm, self).clean()

        has_error = False

        email_str = self.cleaned_data.get('email')
        if email_str is not None and email_str.strip() != '':
            try:
                email = models.Email.objects.get(email=email_str)

                u = models.User.objects.filter(
                    email=email.id, # User has email
                    registered__isnull=False, # User is registered
                    django_user__isnull=False # User has a Django user linked
                ).first()

                if u is not None:
                    self.add_error('email', 'This email belongs to an existing user.')
                    has_error = True
            except models.Email.DoesNotExist:
                # Good - email is not in used
                pass
        
        ph_str = str(self.cleaned_data.get('phone_number'))
        if ph_str is not None and ph_str.strip() != '':
            parsed_ph = phonenumbers.parse(ph_str, None)

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
                    self.add_error('phone_number', 'This phone number belongs to an existing user.')
                    has_error = True
            except models.PhoneNumber.DoesNotExist:
                # Good - no user has this phone number
                pass

        if (email_str is None or email_str.strip() == '') and\
            (ph_str is None or ph_str.strip() == ''):
            self.add_error('email', 'Specify email and/or phone number.')
            self.add_error('phone_number', 'Specify email and/or phone number.')
            has_error = True

        country_key = self.cleaned_data.get('country')
        if country_key is not None and country_key.strip() != '':
            try:
                _ = commods.Country.objects.get(programmatic_key=country_key)
            except commods.Country.DoesNotExist:
                self.add_error('country', 'This field is required.')    
        else:
            self.add_error('country', 'This field is required.')
        
        if has_error:
            raise ValidationError(None)

class ProfileForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField(required=False)
    phone_number = PhoneNumberField(required=False)

    country = forms.CharField()

    def __init__(self, *args, **kwargs):
        # Make request object passed in a class variable
        self.request = kwargs.pop('request')
        self.last_email = kwargs.pop('last_email')
        self.last_phone_number = kwargs.pop('last_phone_number')
        super().__init__(*args, **kwargs)

    def clean(self):
        super(ProfileForm, self).clean()

        has_error = False

        email_str = self.cleaned_data.get('email')
        ph_str = self.cleaned_data.get('phone_number')

        if ph_str is not None:
            ph_str = str(ph_str)

        if (email_str is None or email_str.strip() == '') and\
            (ph_str is None or ph_str.strip() == ''):
            self.add_error('email', 'Specify phone number and/or email.')
            self.add_error('phone_number', 'Specify phone number and/or email.')
            has_error = True

        if email_str is not None and email_str.strip() != '' and self.last_email != email_str:
            try:
                email = models.Email.objects.get(email=email_str)

                u = models.User.objects.filter(
                    email=email.id, # User has email
                    registered__isnull=False, # User is registered
                    django_user__isnull=False # User has a Django user linked
                ).first()

                if u is not None:
                    self.add_error('email', 'This email belongs to an existing user.')
                    has_error = True
            except models.Email.DoesNotExist:
                # Good - email is not in used
                pass

        if ph_str is not None and ph_str.strip() != '' and self.last_phone_number != ph_str:
            parsed_ph = phonenumbers.parse(ph_str, None)
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

                if user_w_ph is not None and self.request.user.user.id != user_w_ph.id:
                    self.add_error('phone_number', 'This phone number belongs to an existing user.')
                    has_error = True
            except models.PhoneNumber.DoesNotExist:
                # Good - no user has this phone number
                pass

        if has_error:
            raise ValidationError(None)

class PasswordChangeForm(forms.Form):
    password = forms.CharField(min_length=8)
    confirm_password = forms.CharField(min_length=8)

    def clean(self):
        super(PasswordChangeForm, self).clean()

        has_error = False

        password = self.cleaned_data.get('password')
        confirm = self.cleaned_data.get('confirm_password')
        if password != confirm:
            self.add_error('password', 'Password doesn\'t match confirm password.')
            self.add_error('confirm_password', 'Password doesn\'t match confirm password.')
            has_error = True
        
        if has_error:
            raise ValidationError(None)














# from urllib import request
# from common.utilities.is_censored import is_censored

# _require_msg = 'This field is required.'
# _censor_msg = 'Don\'t share contact details here. You may share contact details later.'

# class UserEditForm(forms.Form):
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

#     has_company = forms.BooleanField(required=False)

#     # Validated only if has_company is checked.
#     company_name = forms.CharField(
#         required=False,
#         max_length=50
#     )

#     goods_string = forms.CharField(
#         required=True,
#         min_length=1,
#         max_length=200
#     )

#     # No validations, for survey only.
#     is_buyer = forms.BooleanField(required=False)
#     is_seller = forms.BooleanField(required=False)
#     is_buy_agent = forms.BooleanField(required=False)
#     is_sell_agent = forms.BooleanField(required=False)

#     languages_string = forms.CharField(
#         required=True,
#         min_length=1,
#         max_length=200
#     )

#     # Next URL after registration
#     next = forms.CharField(required=False)

#     def clean(self):
#         super(UserEditForm, self).clean()

#         has_error = False

#         if self.cleaned_data.get('has_company'):
#             company_name = self.cleaned_data.get('company_name')
#             if company_name is None or company_name.strip() == '':
#                 self.add_error('company_name', _require_msg)
#                 has_error = True

#         if has_error:
#             raise ValidationError(None)

#         return self.cleaned_data

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

#     has_company = forms.BooleanField(required=False)

#     # Validated only if has_company is checked.
#     company_name = forms.CharField(required=False)
    
#     email = forms.EmailField(
#         required=True
#     )

#     goods_string = forms.CharField(
#         required=True,
#         min_length=1,
#         max_length=200
#     )

#     # No validations, for survey only.
#     is_buyer = forms.BooleanField(required=False)
#     is_seller = forms.BooleanField(required=False)
#     is_buy_agent = forms.BooleanField(required=False)
#     is_sell_agent = forms.BooleanField(required=False)

#     languages_string = forms.CharField(
#         required=True,
#         min_length=1,
#         max_length=200
#     )

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
#                 self.add_error('company_name', _require_msg)
#                 has_error = True

#         if has_error:
#             raise ValidationError(None)

#         return self.cleaned_data

# class WhatsAppBodyForm(forms.Form):
#     body = forms.CharField()

# class LoginForm(forms.Form):
#     whatsapp_phone_number = PhoneNumberField(required=True)
#     next = forms.CharField(required=False)

#     def clean(self):
#         super(LoginForm, self).clean()

#         # Parse phone number
#         try:
#             ph_str = self.cleaned_data.get('whatsapp_phone_number')
#             parsed_ph = phonenumbers.parse(str(ph_str), None)
#             ph_cc = parsed_ph.country_code
#             ph_nn = parsed_ph.national_number
#         except Exception as e:
#             raise ValidationError(None)

#         # Check existence of phone number
#         try:
#             phone_number = models.PhoneNumber.objects.get(
#                 country_code=ph_cc,
#                 national_number=ph_nn
#             )
#         except models.PhoneNumber.DoesNotExist:
#             self.add_error('whatsapp_phone_number', "Account don't exist.")
#             raise ValidationError(None)

#         user = models.User.objects.filter(
#             phone_number=phone_number.id, # User has phone number
#             registered__isnull=False, # User is registered
#             django_user__isnull=False # User has a Django user linked
#         ).first()

#         # Check existence of user
#         if user is None:
#             self.add_error('whatsapp_phone_number', "Account don't exist.")
#             raise ValidationError(None)

#         return self.cleaned_data