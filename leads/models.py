from django.db import models
from django import forms

class Lead(models.Model):
    name = models.CharField(max_length=100)
    # We don't use an IP address field because we want to store whatever value
    # we can capture - whether or not it is valid.
    ip_address = models.CharField('IP Address',
        max_length=100, blank=True, null=True, default=None)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, default=None)
    email = models.EmailField()
    chat_app = models.CharField(max_length=20, choices=(
        ('whatsapp', "WhatsApp"),
        ('wechat', "WeChat")
    ))
    whatsapp_no = models.CharField('WhatsApp Phone Number',
        max_length=50, blank=True, null=True, default=None)
    wechat_no = models.CharField('WeChat Phone Number',
        max_length=50, blank=True, null=True, default=None)
    i_want_to = models.CharField('Role', max_length=20, choices=(
        ('buy', "Buy"),
        ('sell', "Sell"),
        ('buy_sell', "Buy and Sell")
    ))
    i_am_interested_to_buy = models.TextField(
        blank=True, null=True, default=None)

    def __str__(self):
        """Primarily used in administration console."""
        return '%s, %s, %s, %s' % (
            self.name,
            self.email,
            self.chat_app,
            self.i_want_to
        )
    
class LeadModelForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(LeadModelForm, self).clean()
        errors = {}

        # Make sure the user provide the contact details for the contact method
        # he has specified.
        chat_app = cleaned_data.get('chat_app', None)
        whatsapp_no = cleaned_data.get('whatsapp_no', None)
        wechat_no = cleaned_data.get('wechat_no', None)
        if chat_app == 'whatsapp' and whatsapp_no == None:
            errors['whatsapp_no'] = 'Please provide your WhatsApp number.'
        elif chat_app == 'wechat' and wechat_no == None:
            errors['wechat_no'] = 'Please provide your WeChat number.'
        
        # Make sure the user tells us what he is interested to buy - if he says
        # that he is interested in buying.
        i_want_to = cleaned_data.get('i_want_to', None)
        i_am_interested_to_buy = cleaned_data.get('i_am_interested_to_buy', None)
        if (i_want_to == 'buy' or i_want_to == 'buy_sell') and \
            (i_am_interested_to_buy == '' or i_am_interested_to_buy == None):
            errors['i_am_interested_to_buy'] = 'Please tell us what you are interested to buy.'

        raise forms.ValidationError(errors)

    class Meta:
        model = Lead
        fields = [
            'name',
            'email',
            'ip_address',
            'chat_app',
            'whatsapp_no',
            'wechat_no',
            'i_want_to',
            'i_am_interested_to_buy'
        ]