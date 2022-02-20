from django import forms
from django.core.exceptions import ValidationError

from everybase import settings

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

    def clean(self):
        super(LeadForm, self).clean()

        has_error = False
        msg = 'This field is required.'

        # Helper function to get cleaned data
        get = lambda s : self.cleaned_data.get(s)

        # Helper function to test for empty string
        is_empty_string = lambda s : s is None or len(s.strip()) == 0

        if get('need_agent'):
            ct = get('commission_type')
            if ct == 'other':
                if is_empty_string(get('commission_type_other')):
                    self.add_error('commission_type_other', msg)
                    has_error = True
            elif ct == 'percentage':
                if get('commission') is None:
                    self.add_error('commission', msg)
                    has_error = True

                if get('avg_deal_size') is None:
                    self.add_error('avg_deal_size', msg)
                    has_error = True

            if get('commission_payable_after') == 'other':
                if is_empty_string(get('commission_payable_after_other')):
                    self.add_error('commission_payable_after_other', msg)
                    has_error = True

            if get('author_type') == 'broker':
                if is_empty_string(get('commission_payable_by')):
                    self.add_error('commission_payable_by', msg)
                    has_error = True

            if is_empty_string(get('commission_payable_after')):
                self.add_error('commission_payable_after', msg)
                has_error = True

        image_one = get('image_one')
        if image_one is not None and image_one.size > settings.MAX_UPLOAD_SIZE:
            self.add_error('image_one', 'Please upload a smaller file')
            has_error = True

        image_two = get('image_two')
        if image_two is not None and image_two.size > settings.MAX_UPLOAD_SIZE:
            self.add_error('image_two', 'Please upload a smaller file')
            has_error = True

        image_three = get('image_three')
        if image_three is not None and image_three.size > settings.MAX_UPLOAD_SIZE:
            self.add_error('image_three', 'Please upload a smaller file')
            has_error = True

        if has_error:
            raise ValidationError(None)

        return self.cleaned_data