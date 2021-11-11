from django import forms
from django.contrib.postgres.forms import SimpleArrayField
from django.core.exceptions import ValidationError

from . import models

class LeadForm(forms.Form):
    title = forms.CharField(
        required=True,
        min_length=1,
        max_length=200
    )
    details = forms.CharField(required=True)
    lead_type = forms.CharField(required=True)
    author_type = forms.CharField(required=True)
    country_string = forms.CharField(
        required=True,
        min_length=1,
        max_length=20
    )
    commission_pct = forms.FloatField()
    commission_payable_by = forms.CharField()
    commission_payable_after = forms.CharField()
    commission_payable_after_others = forms.CharField()
    other_commission_details = forms.CharField()
    files = forms.CharField()