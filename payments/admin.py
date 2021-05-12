from django.contrib import admin

from . import models as mod
from common import admin as comadm

_payment_link_fields = ['started', 'succeeded', 'failed', 'session_id',
    'currency', 'unit_amount']
@admin.register(mod.PaymentLink)
class PaymentLinkAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _payment_link_fields
    list_editable = comadm.standard_list_editable + _payment_link_fields
    list_filter = comadm.standard_list_filter + ['started', 'succeeded',
        'failed', 'currency']
    search_fields = comadm.standard_search_fields + ['session_id']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _payment_link_fields})
    ]

_payment_event_fields = ['event_type', 'currency', 'amount', 'user',
    'payment_link']
@admin.register(mod.PaymentEvent)
class PaymentEventAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _payment_event_fields
    list_editable = comadm.standard_list_editable + _payment_event_fields
    list_filter = comadm.standard_list_filter + ['event_type', 'currency']
    search_fields = comadm.standard_search_fields + ['user__name']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _payment_event_fields})
    ]
    autocomplete_fields = ['event_type', 'currency', 'user', 'payment_link']

@admin.register(mod.PaymentEventType)
class PaymentEventTypeAdmin(comadm.ChoiceAdmin):
    pass 

@admin.register(mod.Currency)
class CurrencyAdmin(comadm.ChoiceAdmin):
    pass