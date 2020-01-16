from django import forms

class MaterialForm(forms.Form):
    name = forms.CharField(required=True, max_length=100)
    code = forms.CharField(required=True, max_length=100)