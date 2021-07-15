from django.contrib import admin

from . import models as mod
from common import admin as comadm

_payment_hash_fields = ['user', 'match', 'started', 'succeeded', 'failed',
    'session_id']
@admin.register(mod.PaymentHash)
class PaymentHashAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _payment_hash_fields
    list_editable = comadm.standard_list_editable + _payment_hash_fields
    list_filter = comadm.standard_list_filter + ['started', 'succeeded',
        'failed']
    search_fields = comadm.standard_search_fields + ['user__name', 'session_id']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _payment_hash_fields})
    ]
    autocomplete_fields = ['user', 'match']

_payment_event_fields = ['event_type', 'currency', 'amount', 'user',
    'payment_hash']
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
    autocomplete_fields = ['event_type', 'currency', 'user', 'payment_hash']

@admin.register(mod.PaymentEventType)
class PaymentEventTypeAdmin(comadm.ChoiceAdmin):
    pass 

@admin.register(mod.Currency)
class CurrencyAdmin(comadm.ChoiceAdmin):
    pass

@admin.register(mod.Price)
class PriceAdmin(comadm.ChoiceAdmin):
    pass