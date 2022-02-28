from django import forms
from django.core.exceptions import ValidationError
from everybase import settings
from files import models as fimods
from files.utilities.cache_image import cache_image
from files.utilities.delete_cached_image import delete_cached_image

class LeadForm(forms.Form):
    lead_type = forms.CharField()
    author_type = forms.CharField()
    buy_country = forms.CharField()
    sell_country = forms.CharField()
    details = forms.CharField()
    image_one = forms.ImageField(required=False)
    image_two = forms.ImageField(required=False)
    image_three = forms.ImageField(required=False)
    need_agent = forms.BooleanField(required=False) # Unchecked is None

    # These fields will be set only if there are errors in the form. In that
    # case, we'll cache the images, and pass the file ID and cache image URL
    # back to the template via errors. Where these values exists in errors,
    # hidden fields in the form will set these values.
    image_one_cache_use = forms.CharField(required=False)
    image_one_cache_file_id = forms.CharField(required=False)
    image_one_cache_url = forms.CharField(required=False)
    image_two_cache_use = forms.CharField(required=False)
    image_two_cache_file_id = forms.CharField(required=False)
    image_two_cache_url = forms.CharField(required=False)
    image_three_cache_use = forms.CharField(required=False)
    image_three_cache_file_id = forms.CharField(required=False)
    image_three_cache_url = forms.CharField(required=False)

    # Not required whether we need agents or not
    other_agent_details = forms.CharField(required=False)

    ## Following fields are only required if need_agent is True. All of them
    ## are required=False by default.

    commission_type = forms.CharField(required=False)

    # This field is required if commission_type is 'other'
    commission_type_other = forms.CharField(required=False)

    # These fields are required if commission_type is 'percentage'
    commission = forms.FloatField(
        required=False,
        min_value=0.01,
        max_value=100
    )
    avg_deal_size = forms.FloatField(
        required=False,
        min_value=1
    )

    # This field is required if commission_payable_after is 'other'
    commission_payable_after_other = forms.CharField(required=False)

    # Required if author_type is 'broker'
    commission_payable_by = forms.CharField(required=False)

    is_comm_negotiable = forms.BooleanField(required=False) # Unchecked is None
    commission_payable_after = forms.CharField(required=False)

    need_logistics_agent = forms.BooleanField(required=False)
    other_logistics_agent_details = forms.CharField(required=False)

    def clean(self):
        super(LeadForm, self).clean()

        has_error = False

        # Helper function to get cleaned data
        get = lambda s : self.cleaned_data.get(s)

        # Helper function to test for empty string
        is_empty_string = lambda s : s is None or len(s.strip()) == 0

        if get('need_agent'):
            ct = get('commission_type')
            if ct == 'other':
                if is_empty_string(get('commission_type_other')):
                    self.add_error('commission_type_other', 'This field is required.')
                    has_error = True
            elif ct == 'percentage':
                if get('commission') is None:
                    self.add_error('commission', 'This field is required.')
                    has_error = True

                if get('avg_deal_size') is None:
                    self.add_error('avg_deal_size', 'This field is required.')
                    has_error = True

            if get('commission_payable_after') == 'other':
                if is_empty_string(get('commission_payable_after_other')):
                    self.add_error('commission_payable_after_other', 'This field is required.')
                    has_error = True

            if get('author_type') == 'broker':
                if is_empty_string(get('commission_payable_by')):
                    self.add_error('commission_payable_by', 'This field is required.')
                    has_error = True

            if is_empty_string(get('commission_payable_after')):
                self.add_error('commission_payable_after', 'This field is required.')
                has_error = True

        need_logistics_agent = get('need_logistics_agent')
        if need_logistics_agent == True:
            if is_empty_string(get('other_logistics_agent_details')):
                self.add_error('other_logistics_agent_details', 'This field is required.')

        image_one = get('image_one')
        image_two = get('image_two')
        image_three = get('image_three')

        image_one_cache_use = get('image_one_cache_use')
        image_one_cache_file_id = get('image_one_cache_file_id')
        image_one_cache_url = get('image_one_cache_url')

        image_two_cache_use = get('image_two_cache_use')
        image_two_cache_file_id = get('image_two_cache_file_id')
        image_two_cache_url = get('image_two_cache_url')

        image_three_cache_use = get('image_three_cache_use')
        image_three_cache_file_id = get('image_three_cache_file_id')
        image_three_cache_url = get('image_three_cache_url')

        # If file exists, check for cache. If cache exists - delete it.

        # If file passes validation, take note of it, and leave it in request.
        # At the end of the form, if there are other errors, cache the file, and
        # return cache details to template. Otherwise, the file is left in
        # request to be worked with in view. In view, we'll detect an invalid
        # cache and a file in request - letting us choose to work with file.

        # If file fails validation, raise error. It won't be cached.

        # If file do not exist, check for cache. If cache is valid but its flag
        # says we shouldn't use it, the user has indicated to delete it in the
        # frontend - delete it.

        ##### start: image one #####
        cache_image_one = False
        if image_one is not None:
            # Image is not none
            if image_one_cache_file_id is not None and len(image_one_cache_file_id.strip()) != 0:
                # If cache exists, delete it
                delete_cached_image(image_one_cache_file_id)

            if image_one.size > settings.MAX_UPLOAD_SIZE:
                self.add_error('image_one', 'Please upload a smaller file')
                has_error = True
            
            # Cache this image if it has no errors
            cache_image_one = True if not has_error else False
        elif image_one_cache_file_id is not None and len(image_one_cache_file_id.strip()) != 0:
            # Cache exists

            file = fimods.File.objects.get(pk=image_one_cache_file_id)
            if file is not None and file.deleted is None and image_one_cache_use == 'no':
                # Frontend indicated not to use cache, delete it
                delete_cached_image(image_one_cache_file_id)
        ##### end: image one #####

        ##### start: image two #####
        cache_image_two = False
        if image_two is not None:
            # Image is not none
            if image_two_cache_file_id is not None and len(image_two_cache_file_id.strip()) != 0:
                # If cache exists, delete it
                delete_cached_image(image_two_cache_file_id)

            if image_two.size > settings.MAX_UPLOAD_SIZE:
                self.add_error('image_two', 'Please upload a smaller file')
                has_error = True
            
            # Cache this image if it has no errors
            cache_image_two = True if not has_error else False
        elif image_two_cache_file_id is not None and len(image_two_cache_file_id.strip()) != 0:
            # Cache exists

            file = fimods.File.objects.get(pk=image_two_cache_file_id)
            if file is not None and file.deleted is None and image_two_cache_use == 'no':
                # Frontend indicated not to use cache, delete it
                delete_cached_image(image_two_cache_file_id)
        ##### end: image two #####

        ##### start: image three #####
        cache_image_three = False
        if image_three is not None:
            # Image is not none
            if image_three_cache_file_id is not None and len(image_three_cache_file_id.strip()) != 0:
                # If cache exists, delete it
                delete_cached_image(image_three_cache_file_id)

            if image_three.size > settings.MAX_UPLOAD_SIZE:
                self.add_error('image_three', 'Please upload a smaller file')
                has_error = True
            
            # Cache this image if it has no errors
            cache_image_three = True if not has_error else False
        elif image_three_cache_file_id is not None and len(image_three_cache_file_id.strip()) != 0:
            # Cache exists

            file = fimods.File.objects.get(pk=image_three_cache_file_id)
            if file is not None and file.deleted is None and image_three_cache_use == 'no':
                # Frontend indicated not to use cache, delete it
                delete_cached_image(image_three_cache_file_id)
        ##### end: image three #####

        # Cache image it necessary, pass cache details if there's error on form,
        # whether or not it's caused by the image.

        if (has_error or len(self.errors) > 0):
            # has_error tests for errors we test ourselves.
            # len(self.errors) tests for errors from Django Form's default behaviors.

            if cache_image_one:
                fid, url = cache_image(image_one)
                self.add_error(f'image_one_cache_file_id', fid)
                self.add_error(f'image_one_cache_url', url)
            elif image_one_cache_file_id is not None and len(image_one_cache_file_id.strip()) != 0:
                file_one = fimods.File.objects.get(pk=image_one_cache_file_id)
                if file_one.deleted is None:
                    self.add_error(f'image_one_cache_file_id', image_one_cache_file_id)
                    self.add_error(f'image_one_cache_url', image_one_cache_url)

            if cache_image_two:
                fid, url = cache_image(image_two)
                self.add_error(f'image_two_cache_file_id', fid)
                self.add_error(f'image_two_cache_url', url)
            elif image_two_cache_file_id is not None and len(image_two_cache_file_id.strip()) != 0:
                file_two = fimods.File.objects.get(pk=image_two_cache_file_id)
                if file_two.deleted is None:
                    self.add_error(f'image_two_cache_file_id', image_two_cache_file_id)
                    self.add_error(f'image_two_cache_url', image_two_cache_url)

            if cache_image_three:
                fid, url = cache_image(image_three)
                self.add_error(f'image_three_cache_file_id', fid)
                self.add_error(f'image_three_cache_url', url)
            elif image_three_cache_file_id is not None and len(image_three_cache_file_id.strip()) != 0:
                file_three = fimods.File.objects.get(pk=image_three_cache_file_id)
                if file_three.deleted is None:
                    self.add_error(f'image_three_cache_file_id', image_three_cache_file_id)
                    self.add_error(f'image_three_cache_url', image_three_cache_url)

        if has_error:
            raise ValidationError(None)

        return self.cleaned_data