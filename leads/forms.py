from django import forms
from django.core.exceptions import ValidationError

class LeadForm(forms.Form):
    pk = forms.CharField()
    lead_type = forms.CharField()
    buy_country = forms.CharField()
    sell_country = forms.CharField()
    avg_deal_size = forms.FloatField()
    avg_comm_pct = forms.CharField()
    details = forms.CharField()
    other_commission_details = forms.CharField(required=False)

class OldLeadForm(forms.Form):
    title = forms.CharField(
        required=True,
        min_length=1,
        max_length=200
    )
    details = forms.CharField(required=True)
    lead_type = forms.CharField(required=True)
    author_type = forms.CharField(required=True)
    country = forms.CharField(required=True)
    commission_pct = forms.FloatField(required=True)
    commission_payable_by = forms.CharField(required=True)
    commission_payable_after = forms.CharField(required=True)
    commission_payable_after_others = forms.CharField(required=False)
    other_commission_details = forms.CharField(required=False)
    files = forms.CharField(required=False)

    def clean(self):
        super(LeadForm, self).clean()

        if self.cleaned_data.get('commission_payable_after') == 'others':
            others_details = self.cleaned_data.get(
                'commission_payable_after_others')

            if others_details is None or len(others_details) == 0:
                self.add_error('commission_payable_after_others',
                    'Please specify when the commission will be paid.')
                raise ValidationError(None)

        return self.cleaned_data

class ContactForm(forms.Form):
    message = forms.CharField(required=True)