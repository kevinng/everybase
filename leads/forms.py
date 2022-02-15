from django import forms
from django.core.exceptions import ValidationError

class LeadForm(forms.Form):
    lead_type = forms.CharField()
    
    author_type = forms.CharField()
    buy_country = forms.CharField()
    sell_country = forms.CharField()
    details = forms.CharField()
    need_agent = forms.CharField()
    commission_payable_by = forms.CharField()
    commission_type = forms.CharField()
    # Conditionally require in clean()
    commission_type_other = forms.CharField(required=False)
    commissions = forms.FloatField(required=False)
    avg_deal_size = forms.FloatField(required=False)
    commission_payable_after = forms.CharField()
    # Conditionally require in clean()
    commission_payable_after_others = forms.CharField(required=False)
    # Conditionally require in clean()
    other_comm_details = forms.CharField(required=False)

    def clean(self):
        super(LeadForm, self).clean()

        has_error = False

        # Require commission and avg_deal_size if commission_type is
        # 'percentage', require commission_type_other if commission_type is
        # 'other'.
        commission_type = self.cleaned_data.get('commission_type')
        if commission_type == 'percentage':
            commissions = self.cleaned_data.get('commissions')
            if commissions is None or \
                len(commissions.strip()) == 0:
                self.add_error('commissions', 'This field is required.')
                has_error = True

            avg_deal_size = self.cleaned_data.get('avg_deal_size')
            if avg_deal_size is None or \
                len(avg_deal_size.strip()) == 0:
                self.add_error('avg_deal_size', 'This field is required.')
                has_error = True

        elif commission_type == 'other':
            commission_type_other = self.cleaned_data.get(
                'commission_type_other')
            if commission_type_other is None or \
                len(commission_type_other.strip()) == 0:
                self.add_error('commission_type_other',
                    'This field is required.')
                has_error = True

        # Require commission_payable_after_others if commission_payable_after
        # is 'other'.
        if self.cleaned_data.get('commission_payable_after') == 'others':
            commission_payable_after_others = self.cleaned_data.get(
                'commission_payable_after_others')
            if commission_payable_after_others is None or \
                len(commission_payable_after_others.strip()) == 0:
                self.add_error('commission_payable_after_others',
                    'This field is required.')
                has_error = True

        if has_error:
            raise ValidationError(None)

        return self.cleaned_data