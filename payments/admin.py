from django.contrib import admin
from common import admin as comadm
from payments import models

@admin.register(models.Currency)
class CurrencyAdmin(comadm.ChoiceAdmin):
    pass

_stripe_callback_session_fields = ['session_id', 'amount_total', 'currency',
    'customer', 'customer_details_email', 'mode', 'payment_intent',
    'payment_status', 'success_url', 'cancel_url']
@admin.register(models.StripeCallbackSession)
class StripeCallbackSessionAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _stripe_callback_session_fields
    list_editable = comadm.standard_list_editable + _stripe_callback_session_fields
    list_filter = comadm.standard_list_filter + ['currency', 'mode',
        'payment_intent', 'payment_status', 'success_url', 'cancel_url']
    search_fields = comadm.standard_search_fields + ['session_id',
        'customer', 'customer_details_email']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _stripe_callback_session_fields})]

_stripe_checkout_session_fields = ['customer', 'session_id', 'mode',
    'success_url', 'cancel_url']
@admin.register(models.StripeCheckoutSession)
class StripeCheckoutSessionAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _stripe_checkout_session_fields
    list_editable = comadm.standard_list_editable + _stripe_checkout_session_fields
    list_filter = comadm.standard_list_filter + ['mode', 'success_url',
        'cancel_url']
    search_fields = comadm.standard_search_fields + ['customer__api_id',
        'session_id']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _stripe_checkout_session_fields})]
    autocomplete_fields = ['customer']

_stripe_customer_fields = ['user', 'api_id']
@admin.register(models.StripeCustomer)
class StripeCustomerAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _stripe_customer_fields
    list_editable = comadm.standard_list_editable + _stripe_customer_fields
    search_fields = comadm.standard_search_fields + ['user__first_name',
        'user__last_name', 'user__id', 'api_id']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _stripe_customer_fields})]
    autocomplete_fields = ['user']

_stripe_checkout_session_line_item_fields = ['session', 'price', 'quantity']
@admin.register(models.StripeCheckoutSessionLineItem)
class StripeCheckoutSessionLineItemAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + \
        _stripe_checkout_session_line_item_fields
    list_editable = comadm.standard_list_editable + \
        _stripe_checkout_session_line_item_fields
    search_fields = comadm.standard_search_fields + ['session__session_id']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _stripe_checkout_session_line_item_fields})]
    autocomplete_fields = ['session']

_credits_event_fields = ['user', 'value', 'type', 'session', 'notes']
@admin.register(models.CreditsEvent)
class CreditsEventAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _credits_event_fields
    list_editable = comadm.standard_list_editable + _credits_event_fields
    search_fields = comadm.standard_search_fields + ['user__first_name',
        'user__last_name', 'session__session_id', 'notes']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _credits_event_fields})]
    autocomplete_fields = ['user', 'session']