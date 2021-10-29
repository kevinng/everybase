# from django.contrib import admin

# from . import models as mod
# from common import admin as comadm

# _payment_hash_fields = ['user', 'started', 'succeeded', 'failed',
#     'expired', 'session_id', 'price']
# @admin.register(mod.PaymentHash)
# class PaymentHashAdmin(comadm.StandardAdmin):
#     # List page settings
#     list_display = comadm.standard_list_display + _payment_hash_fields
#     list_editable = comadm.standard_list_editable + _payment_hash_fields
#     list_filter = comadm.standard_list_filter + ['started', 'succeeded',
#         'failed', 'price']
#     search_fields = comadm.standard_search_fields + ['user__name', 'session_id']

#     # Details page settings
#     fieldsets = comadm.standard_fieldsets + [
#         ('Details', {'fields': _payment_hash_fields})
#     ]
#     autocomplete_fields = ['user', 'price']

# _payment_event_fields = ['event_type', 'currency', 'amount', 'user',
#     'payment_hash']
# @admin.register(mod.PaymentEvent)
# class PaymentEventAdmin(comadm.StandardAdmin):
#     # List page settings
#     list_display = comadm.standard_list_display + _payment_event_fields
#     list_editable = comadm.standard_list_editable + _payment_event_fields
#     list_filter = comadm.standard_list_filter + ['event_type', 'currency']
#     search_fields = comadm.standard_search_fields + ['user__name']

#     # Details page settings
#     fieldsets = comadm.standard_fieldsets + [
#         ('Details', {'fields': _payment_event_fields})
#     ]
#     autocomplete_fields = ['event_type', 'currency', 'user', 'payment_hash']

# @admin.register(mod.PaymentEventType)
# class PaymentEventTypeAdmin(comadm.ChoiceAdmin):
#     pass 

# @admin.register(mod.Currency)
# class CurrencyAdmin(comadm.ChoiceAdmin):
#     pass

# _price_fields = ['display_name', 'value', 'currency']
# @admin.register(mod.Price)
# class PriceAdmin(comadm.ChoiceAdmin):
#     # List page settings
#     list_display = comadm.choice_list_display + _price_fields
#     list_editable = comadm.choice_list_editable + _price_fields
#     search_fields = comadm.choice_search_fields + _price_fields
#     ordering = comadm.choice_ordering + _price_fields

#     # Details page settings
#     fieldsets = comadm.choice_fieldsets + [
#         ('Details', {'fields': _price_fields})
#     ]
#     autocomplete_fields = ['currency']