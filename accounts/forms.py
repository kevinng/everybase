from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())
    next = forms.CharField(required=False, widget=forms.HiddenInput())

class ResetPasswordForm(forms.Form):
    email = forms.EmailField(required=True)
    next = forms.CharField(required=False, widget=forms.HiddenInput())

class SetPasswordForm(forms.Form):
    password = forms.CharField(required=True, widget=forms.PasswordInput())
    confirm_password = forms.CharField(required=True, widget=forms.PasswordInput())
    code = forms.CharField(required=False, widget=forms.HiddenInput())
    next = forms.CharField(required=False, widget=forms.HiddenInput())

    def clean(self):
        cd = super(SetPasswordForm, self).clean()
        password = cd['password']
        confirm_password = cd['confirm_password']

        if password != confirm_password:
            self.add_error(None, 'Passwords do not match.')
        
        return cd