from django.contrib import admin

from . import models as mod
from common import admin as comadm

_stripe_session_fields = ['started', 'succeeded', 'failed', 'session_id',
    'currency', 'unit_amount']
@admin.register(mod.StripeSession)
class StripeSession(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _stripe_session_fields
    list_editable = comadm.standard_list_editable + _stripe_session_fields
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['started', 'succeeded',
        'failed', 'currency']
    search_fields = comadm.standard_search_fields + ['session_id']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _stripe_session_fields})
    ]

_payment_event_fields = ['event_type', 'currency', 'amount', 'user', 'match',
    'session']
@admin.register(mod.PaymentEvent)
class PaymentEventAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _payment_event_fields
    list_editable = comadm.standard_list_editable + _payment_event_fields
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['event_type', 'currency']
    search_fields = comadm.standard_search_fields + ['user__name']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _payment_event_fields})
    ]
    autocomplete_fields = ['event_type', 'currency', 'user', 'match', 'session']

@admin.register(mod.PaymentEventType)
class PaymentEventTypeAdmin(comadm.ChoiceAdmin):
    pass 

@admin.register(mod.Currency)
class CurrencyAdmin(comadm.ChoiceAdmin):
    pass