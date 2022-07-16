from phonenumber_field.formfields import PhoneNumberField

from django import forms
from common.utilities.is_censored import is_censored
from django.core.exceptions import ValidationError

from leads import models
from relationships.utilities.get_or_create_email import get_or_create_email
from relationships.utilities.get_or_create_phone_number import get_or_create_phone_number

class SignUpSearchNotification(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    country = forms.CharField()
    email = forms.EmailField()
    phone_number = PhoneNumberField()

    via_whatsapp = forms.BooleanField(required=False)
    via_wechat = forms.BooleanField(required=False)
    via_wechat_id = forms.CharField(required=False)

class LeadForm(forms.Form):
    body = forms.CharField()
    lead_type = forms.CharField()

    def clean(self):
        super(LeadForm, self).clean()
        if is_censored(self.cleaned_data.get('body')):
            raise ValidationError({'body': ["Don't include contact details. You'll receive email and phone number - when someone contacts you.",]})

class ContactLeadForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    country = forms.CharField()
    email = forms.EmailField()
    phone_number = PhoneNumberField()

    via_whatsapp = forms.BooleanField(required=False)
    via_wechat = forms.BooleanField(required=False)
    via_wechat_id = forms.CharField(required=False)

    comments = forms.CharField(max_length=100)

    # Required depends on lead type

    to_selling_as_sales_agent = forms.BooleanField(required=False)
    to_selling_as_sourcing_goods = forms.BooleanField(required=False)
    to_selling_as_other = forms.BooleanField(required=False)
    
    to_buying_as_sourcing_agent = forms.BooleanField(required=False)
    to_buying_as_promoting_goods = forms.BooleanField(required=False)
    to_buying_as_other = forms.BooleanField(required=False)
    
    to_sales_agent_as_seeking_cooperation = forms.BooleanField(required=False)
    to_sales_agent_as_sourcing_goods = forms.BooleanField(required=False)
    to_sales_agent_as_other = forms.BooleanField(required=False)
    
    to_sourcing_agent_as_seeking_cooperation = forms.BooleanField(required=False)
    to_sourcing_agent_as_promoting_goods = forms.BooleanField(required=False)
    to_sourcing_agent_as_other = forms.BooleanField(required=False)
    
    to_logistics_agent_as_need_logistics = forms.BooleanField(required=False)
    to_logistics_agent_as_other = forms.BooleanField(required=False)
    
    to_need_logistics_as_logistics_agent = forms.BooleanField(required=False)
    to_need_logistics_as_other = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        # Make request object passed in a class variable
        self.lead = kwargs.pop('lead')
        super().__init__(*args, **kwargs)

    def clean(self):
        super(ContactLeadForm, self).clean()

        via_wechat = self.cleaned_data.get('via_wechat')
        via_wechat_id = self.cleaned_data.get('via_wechat_id')

        err_msg = 'This field is required.'

        if via_wechat is not None and via_wechat == True and (via_wechat_id is None or via_wechat_id.strip() == ''):
            self.add_error('via_wechat_id', err_msg)

        previous_contact = models.Contact.objects.filter(
            lead=self.lead,
            email=get_or_create_email(self.cleaned_data.get('email')),
            phone_number=get_or_create_phone_number(self.cleaned_data.get('phone_number'))
        ).first()

        if previous_contact is not None:
            self.add_error('email', "You've contacted the author of this lead before.")
            self.add_error('phone_number', "You've contacted the author of this lead before.")

class ContactNoteForm(forms.Form):
    body = forms.CharField()
    relevance = forms.CharField()


















# class _LeadForm(forms.Form):
#     lead_type = forms.CharField()
#     # author_type = forms.CharField()
#     country = forms.CharField()
#     headline = forms.CharField()
#     commission_type = forms.CharField()

#     # Non-required fields
#     category = forms.CharField(required=False)
#     commission_usd_mt = forms.DecimalField(required=False)
#     min_commission_percentage = forms.DecimalField(required=False)
#     max_commission_percentage = forms.DecimalField(required=False)
#     details = forms.CharField(required=False)
#     questions = forms.CharField(required=False)

#     def clean(self):
#         super(LeadForm, self).clean()

#         has_error = False
#         country = self.cleaned_data.get('country')
#         commission_type = self.cleaned_data.get('commission_type')
#         commission_usd_mt = self.cleaned_data.get('commission_usd_mt')
#         min_commission_percentage = self.cleaned_data.get('min_commission_percentage')
#         max_commission_percentage = self.cleaned_data.get('max_commission_percentage')

#         headline = self.cleaned_data.get('headline')
#         details = self.cleaned_data.get('details')
#         questions = self.cleaned_data.get('questions')
        
#         if country is not None and country == 'no_country':
#             self.add_error('country', 'This field is required.')
#             has_error = True

#         if min_commission_percentage is not None and max_commission_percentage is not None and commission_type is not None and commission_type == 'percentage':
#             if min_commission_percentage < 0.01 or min_commission_percentage > 100:
#                 self.add_error('min_commission_percentage', 'Agent commission must be between 0.01% and 100%')
#                 has_error = True
            
#             if max_commission_percentage < 0.01 or max_commission_percentage > 100:
#                 self.add_error('max_commission_percentage', 'Agent commission must be between 0.01% and 100%')
#                 has_error = True
            
#             if min_commission_percentage >= max_commission_percentage:
#                 self.add_error('min_commission_percentage', 'Minimum commission must be smaller than maximum commission')
#                 has_error = True
            
#             if max_commission_percentage <= min_commission_percentage:
#                 self.add_error('max_commission_percentage', 'Maximum commission must be greater than minimum commission')
#                 has_error = True
#         elif min_commission_percentage is None and max_commission_percentage is None and commission_type == 'percentage':
#             self.add_error('min_commission_percentage', 'This field is required.')
#             self.add_error('max_commission_percentage', 'This field is required.')
#             has_error = True
#         elif commission_usd_mt is None and commission_type == 'usd_mt':
#             self.add_error('commission_usd_mt', 'This field is required.')
#             has_error = True

#         if headline is not None and is_censored(headline):
#             self.add_error('headline', 'Please do not include contact details.')
#             has_error = True

#         if details is not None and is_censored(details):
#             self.add_error('details', 'Please do not include contact details.')
#             has_error = True

#         if questions is not None and is_censored(questions):
#             self.add_error('questions', 'Please do not include contact details.')
#             has_error = True
        
#         if has_error:
#             raise ValidationError(None)

# class ApplicationForm(forms.Form):
#     has_experience = forms.BooleanField(required=False)
#     has_buyers = forms.BooleanField(required=False)
#     applicant_comments = forms.CharField()
#     answers = forms.CharField(required=False)

# class ApplicationMessageForm(forms.Form):
#     body = forms.CharField()



















# from urllib import request
# from django.core.exceptions import ValidationError
# from everybase import settings
# from files import models as fimods
# from files.utilities.cache_image import cache_image
# from files.utilities.delete_file import delete_file
# from common.utilities.is_censored import is_censored

# _require_msg = 'This field is required.'
# _censor_msg = 'Don\'t share contact details here. You may share contact details later.'

# def _handle_lead_image(form, image, file_id, cache_use):
#     cache_if_form_error = False
#     has_error = False
#     deleted = False
#     if image is not None:
#         # Image is not none
#         if file_id is not None and len(file_id.strip()) != 0:
#             # If cache exists, delete it
#             delete_file(file_id)

#         if image.size > settings.MAX_UPLOAD_SIZE:
#             form.add_error('image_one', 'Please upload a smaller file')
#             has_error = True
        
#         # Cache this image if it has no errors
#         cache_if_form_error = True if not has_error else False
#     elif file_id is not None and len(file_id.strip()) != 0:
#         # Cache exists

#         file = fimods.File.objects.get(pk=file_id)
#         if file is not None and file.deleted is None and cache_use == 'no':
#             # Frontend indicated not to use cache, delete it
#             delete_file(file_id)
#             deleted = True

#     # Will cache image and does image have error
#     return cache_if_form_error, has_error, deleted

# class LeadForm(forms.Form):
#     lead_type = forms.CharField()
#     currency = forms.CharField()
#     author_type = forms.CharField()
#     buy_country = forms.CharField()
#     sell_country = forms.CharField()
#     headline = forms.CharField()
#     details = forms.CharField()
#     agent_job = forms.CharField()

#     image_one = forms.ImageField(required=False)
#     image_two = forms.ImageField(required=False)
#     image_three = forms.ImageField(required=False)

#     commission_type = forms.CharField(required=False)

#     # These fields are required if commission_type is 'earning'
#     commission_earnings = forms.FloatField(required=False)
#     commission_quantity_unit_string = forms.CharField(required=False)

#     # These field is required if commission_type is 'percentage'
#     commission_percentage = forms.FloatField(
#         required=False,
#         min_value=0.01,
#         max_value=100
#     )

#     # This field is required if commission_type is 'other'
#     commission_type_other = forms.CharField(required=False)

#     # Not required, only used if commission_type is NOT 'other'
#     other_comm_details = forms.CharField(required=False)

#     # Required if author_type is 'broker'
#     commission_payable_by = forms.CharField(required=False)

#     # Always required
#     commission_payable_after = forms.CharField(required=False)

#     # This field is required if commission_payable_after is 'other'
#     commission_payable_after_other = forms.CharField(required=False)

#     is_comm_negotiable = forms.BooleanField(required=False) # Unchecked is None

#     question_1 = forms.CharField()
#     question_2 = forms.CharField()
#     question_3 = forms.CharField(required=False) # Optional question

#     # These fields will be set only if there are errors in the form. In that
#     # case, we'll cache the images, and pass the file ID and cache image URL
#     # back to the template via errors. Where these values exists in errors,
#     # hidden fields in the form will set these values.
#     image_one_cache_use = forms.CharField(required=False)
#     image_one_cache_file_id = forms.CharField(required=False)
#     image_one_cache_url = forms.CharField(required=False)
#     image_two_cache_use = forms.CharField(required=False)
#     image_two_cache_file_id = forms.CharField(required=False)
#     image_two_cache_url = forms.CharField(required=False)
#     image_three_cache_use = forms.CharField(required=False)
#     image_three_cache_file_id = forms.CharField(required=False)
#     image_three_cache_url = forms.CharField(required=False)

#     def clean(self):
#         super(LeadForm, self).clean()

#         has_error = False

#         # Helper function to get cleaned data
#         get = lambda s : self.cleaned_data.get(s)

#         # Helper function to test for empty string
#         is_empty_string = lambda s : s is None or len(str(s).strip()) == 0

#         ct = get('commission_type')
#         if ct == 'percentage':
#             if is_empty_string(get('commission_percentage')):
#                 self.add_error('commission_percentage', _require_msg)
#                 has_error = True
#         elif ct == 'earning':
#             if is_empty_string(get('commission_earnings')):
#                 self.add_error('commission_earnings', _require_msg)
#                 has_error = True
#             elif is_empty_string(get('commission_quantity_unit_string')):
#                 self.add_error('commission_quantity_unit_string', _require_msg)
#                 has_error = True
#         elif ct == 'other':
#             if is_empty_string(get('commission_type_other')):
#                 self.add_error('commission_type_other', _require_msg)
#                 has_error = True

#         if get('commission_payable_after') == 'other':
#             if is_empty_string(get('commission_payable_after_other')):
#                 self.add_error('commission_payable_after_other', _require_msg)
#                 has_error = True

#         if get('author_type') == 'broker':
#             if is_empty_string(get('commission_payable_by')):
#                 self.add_error('commission_payable_by', _require_msg)
#                 has_error = True

#         image_one = get('image_one')
#         image_two = get('image_two')
#         image_three = get('image_three')

#         image_one_cache_use = get('image_one_cache_use')
#         image_one_cache_file_id = get('image_one_cache_file_id')
#         image_one_cache_url = get('image_one_cache_url')

#         image_two_cache_use = get('image_two_cache_use')
#         image_two_cache_file_id = get('image_two_cache_file_id')
#         image_two_cache_url = get('image_two_cache_url')

#         image_three_cache_use = get('image_three_cache_use')
#         image_three_cache_file_id = get('image_three_cache_file_id')
#         image_three_cache_url = get('image_three_cache_url')

#         # If file exists, check for cache. If cache exists - delete it.

#         # If file passes validation, take note of it, and leave it in request.
#         # At the end of the form, if there are other errors, cache the file, and
#         # return cache details to template. Otherwise, the file is left in
#         # request to be worked with in view. In view, we'll detect an invalid
#         # cache and a file in request - letting us choose to work with file.

#         # If file fails validation, raise error. It won't be cached.

#         # If file do not exist, check for cache. If cache is valid but its flag
#         # says we shouldn't use it, the user has indicated to delete it in the
#         # frontend - delete it.

#         # Image one
#         cache_image_one_if_form_error, image_one_has_error, _ = _handle_lead_image(
#             self,
#             image_one,
#             image_one_cache_file_id,
#             image_one_cache_use
#         )
#         has_error = image_one_has_error if image_one_has_error else has_error

#         # Image two
#         cache_image_two_if_form_error, image_two_has_error, _ = _handle_lead_image(
#             self,
#             image_two,
#             image_two_cache_file_id,
#             image_two_cache_use
#         )
#         has_error = image_two_has_error if image_two_has_error else has_error

#         # Image three
#         cache_image_three_if_form_error, image_three_has_error, _ = _handle_lead_image(
#             self,
#             image_three,
#             image_three_cache_file_id,
#             image_three_cache_use
#         )
#         has_error = image_three_has_error if image_three_has_error else has_error

#         # Cache image it necessary, pass cache details if there's error on form,
#         # whether or not it's caused by the image.

#         if (has_error or len(self.errors) > 0):
#             # has_error tests for custom errors
#             # len(self.errors) tests for Django default errors

#             # Cache image or pass file ID/URL if it's not deleted

#             if cache_image_one_if_form_error:
#                 fid, url = cache_image(image_one)
#                 self.add_error('image_one_cache_file_id', fid)
#                 self.add_error('image_one_cache_url', url)
#             elif not is_empty_string(image_one_cache_file_id):
#                 file_one = fimods.File.objects.get(pk=image_one_cache_file_id)
#                 if file_one.deleted is None:
#                     self.add_error('image_one_cache_file_id', image_one_cache_file_id)
#                     self.add_error('image_one_cache_url', image_one_cache_url)

#             if cache_image_two_if_form_error:
#                 fid, url = cache_image(image_two)
#                 self.add_error('image_two_cache_file_id', fid)
#                 self.add_error('image_two_cache_url', url)
#             elif not is_empty_string(image_two_cache_file_id):
#                 file_two = fimods.File.objects.get(pk=image_two_cache_file_id)
#                 if file_two.deleted is None:
#                     self.add_error('image_two_cache_file_id', image_two_cache_file_id)
#                     self.add_error('image_two_cache_url', image_two_cache_url)

#             if cache_image_three_if_form_error:
#                 fid, url = cache_image(image_three)
#                 self.add_error('image_three_cache_file_id', fid)
#                 self.add_error('image_three_cache_url', url)
#             elif not is_empty_string(image_three_cache_file_id):
#                 file_three = fimods.File.objects.get(pk=image_three_cache_file_id)
#                 if file_three.deleted is None:
#                     self.add_error('image_three_cache_file_id', image_three_cache_file_id)
#                     self.add_error('image_three_cache_url', image_three_cache_url)

#         if has_error:
#             raise ValidationError(None)

#         return self.cleaned_data

# class ApplicationFormNoQ3(forms.Form):
#     answer_1 = forms.CharField()
#     answer_2 = forms.CharField()
#     answer_3 = forms.CharField(required=False)
#     applicant_comments = forms.CharField(required=False)

# class ApplicationFormQ3(forms.Form):
#     answer_1 = forms.CharField()
#     answer_2 = forms.CharField()
#     answer_3 = forms.CharField()
#     applicant_comments = forms.CharField(required=False)

# class ApplicationDetailForm(forms.Form):
#     purpose = forms.CharField()

#     # Required if purpose is 'message'
#     body = forms.CharField(required=False)

#     def clean(self):
#         super(ApplicationDetailForm, self).clean()

#         has_error = False

#         if self.cleaned_data.get('purpose') == 'message':
#             body = self.cleaned_data.get('body')
#             if body is None or body.strip() == '':
#                 self.add_error('body', _require_msg)
#                 has_error = True

#         if has_error:
#             raise ValidationError(None)

#         return self.cleaned_data