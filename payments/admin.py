from django.contrib import admin
from common import admin as comadm
from payments import models

@admin.register(models.Currency)
class CurrencyAdmin(comadm.ChoiceAdmin):
    pass

_stripe_price_fields = ['price_id', 'name', 'currency', 'value']
@admin.register(models.StripePrice)
class StripePriceAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _stripe_price_fields
    list_editable = comadm.standard_list_editable + _stripe_price_fields
    search_fields = comadm.standard_search_fields + ['price_id', 'name']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _stripe_price_fields})]
    autocomplete_fields = ['currency']

_stripe_event_fields = ['event_id', 'amount_total', 'currency',
    'customer', 'customer_details_email', 'mode', 'payment_intent',
    'payment_status', 'success_url', 'cancel_url']
@admin.register(models.StripeEvent)
class StripeEventAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _stripe_event_fields
    list_editable = [] # Speed up loading
    list_filter = comadm.standard_list_filter + ['currency', 'mode',
        'payment_intent', 'payment_status']
    search_fields = comadm.standard_search_fields + ['event_id', 'customer',
        'customer_details_email']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _stripe_event_fields})]

_stripe_customer_fields = ['user', 'customer_id']
@admin.register(models.StripeCustomer)
class StripeCustomerAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _stripe_customer_fields
    list_editable = [] # Speed up loading
    search_fields = comadm.standard_search_fields + ['user__first_name',
        'user__last_name', 'user__id', 'customer_id']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _stripe_customer_fields})]
    autocomplete_fields = ['user']

_stripe_checkout_session_fields = ['contact_user_credits_bundle',
    'alert_notification_credits_bundle', 'subscription_plan',
    'customer', 'session_id', 'mode']
@admin.register(models.StripeCheckoutSession)
class StripeCheckoutSessionAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + \
        _stripe_checkout_session_fields
    list_editable = [] # Speed up loading
    list_filter = comadm.standard_list_filter + ['mode']
    search_fields = comadm.standard_search_fields + ['customer__customer_id',
        'session_id']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _stripe_checkout_session_fields})]
    autocomplete_fields = ['customer']

_stripe_checkout_session_line_item_fields = ['session', 'price', 'quantity']
@admin.register(models.StripeCheckoutSessionLineItem)
class StripeCheckoutSessionLineItemAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + \
        _stripe_checkout_session_line_item_fields
    list_editable = [] # Speed up loading
    search_fields = comadm.standard_search_fields + ['session__session_id']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _stripe_checkout_session_line_item_fields})]
    autocomplete_fields = ['session']

# Business Model

_subscription_plan_fields = ['name', 'price_id', 'contact_user_credits_per_day',
    'alert_notification_credits_per_month']
@admin.register(models.SubscriptionPlan)
class SubscriptionPlanAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _subscription_plan_fields
    list_editable = [] # Speed up loading
    search_fields = comadm.standard_search_fields + ['name', 'price_id']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _subscription_plan_fields})]

_contact_user_credits_bundle_fields = ['name', 'price_id', 'credits',
    'expiry_days', 'plan_bonus_credits']
@admin.register(models.ContactUserCreditsBundle)
class ContactUserCreditsBundleAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + \
        _contact_user_credits_bundle_fields
    list_editable = [] # Speed up loading
    search_fields = comadm.standard_search_fields + ['name', 'price_id']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _contact_user_credits_bundle_fields})]

_alert_notification_credits_bundle_fields = ['name', 'price_id', 'credits',
    'expiry_days', 'plan_bonus_credits']
@admin.register(models.AlertNotificationCreditsBundle)
class AlertNotificationCreditsBundleAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + \
        _alert_notification_credits_bundle_fields
    list_editable = [] # Speed up loading
    search_fields = comadm.standard_search_fields + ['name', 'price_id']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _alert_notification_credits_bundle_fields})]

_user_subscription_plan_fields = ['user', 'started', 'renewed', 'expire',
    'plan', 'last_plan', 'contact_user_credits_refreshed',
    'contact_user_credits', 'alert_notification_credits_refreshed',
    'alert_notification_credits']
@admin.register(models.UserSubscriptionPlan)
class UserSubscriptionPlanAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _user_subscription_plan_fields
    list_editable = [] # Speed up loading
    search_fields = comadm.standard_search_fields + ['user__first_name',
        'user__last_name']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _user_subscription_plan_fields})]

_user_contact_user_credits_bundle_fields = ['user', 'bundle', 'started',
    'expire', 'credits_added', 'credits_left']
@admin.register(models.UserContactUserCreditsBundle)
class UserContactUserCreditsBundleAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + \
        _user_contact_user_credits_bundle_fields
    list_editable = [] # Speed up loading
    search_fields = comadm.standard_search_fields + ['user__first_name',
        'user__last_name']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _user_contact_user_credits_bundle_fields})]

_user_alert_notification_credits_bundle_fields = ['user', 'bundle', 'started',
    'expire', 'credits_added', 'credits_left']
@admin.register(models.UserAlertNotificationCreditsBundle)
class UserAlertNotificationCreditsBundleAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + \
        _user_alert_notification_credits_bundle_fields
    list_editable = []
    search_fields = comadm.standard_search_fields + ['user__first_name',
        'user__last_name']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': \
            _user_alert_notification_credits_bundle_fields})]