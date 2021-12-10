from django.contrib import admin
from common import admin as comadm
from leads import models

_lead_fields = ['author', 'lead_type', 'author_type', 'title', 'details',
    'country', 'commission_pct', 'commission_payable_after',
    'other_commission_details', 'internal_notes', 'onboarding', 'onboarded']
@admin.register(models.Lead)
class LeadAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['uuid'] + _lead_fields
    list_editable = comadm.standard_list_editable + _lead_fields
    list_filter = comadm.standard_list_filter + ['lead_type', 'author_type',
        'country', 'commission_payable_after', 'onboarding', 'onboarded']
    search_fields = comadm.standard_search_fields + ['title', 'details',
        'other_commission_details', 'internal_notes']

    # Details page settings
    readonly_fields = comadm.standard_readonly_fields + ['uuid']
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _lead_fields})]
    autocomplete_fields = ['author', 'country']

_saved_lead_fields = ['saved', 'saver', 'lead']
@admin.register(models.SavedLead)
class SavedLeadAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _saved_lead_fields
    list_editable = comadm.standard_list_editable + _saved_lead_fields
    list_filter = comadm.standard_list_filter + ['saved']
    search_fields = comadm.standard_search_fields + ['saver__id',
        'saver__family_first_name', 'saver__family_last_name',
        'lead__id', 'lead__title', 'lead__description']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _saved_lead_fields})]
    autocomplete_fields = ['saver', 'lead']

_lead_detail_access_fields = ['lead', 'accessor', 'access_count']
@admin.register(models.LeadDetailAccess)
class LeadDetailAccessAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _lead_detail_access_fields
    list_editable = comadm.standard_list_editable + _lead_detail_access_fields
    list_filter = comadm.standard_list_filter
    search_fields = comadm.standard_search_fields + ['accessor__first_name',
        'accessor__last_name']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _lead_detail_access_fields})]
    autocomplete_fields = ['lead', 'accessor']

_contact_request_fields = ['response', 'contactor', 'lead', 'message']
@admin.register(models.ContactRequest)
class ContactRequestAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _contact_request_fields
    list_editable = comadm.standard_list_editable + _contact_request_fields
    search_fields = comadm.standard_search_fields + ['contactor__first_name',
        'contactor__last_name', 'lead__author__first_name',
        'lead__author__last_name']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _contact_request_fields})]
    autocomplete_fields = ['contactor', 'lead']

_filter_form_post_fields = ['title', 'details', 'is_buying', 'is_selling',
'is_direct', 'is_agent', 'user_country', 'lead_country', 'is_initial_deposit',
'is_goods_shipped', 'is_payment_received', 'is_goods_received', 'is_others',
'user']
@admin.register(models.FilterFormPost)
class FilterFormPostAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _filter_form_post_fields
    list_editable = comadm.standard_list_editable + _filter_form_post_fields
    search_fields = comadm.standard_search_fields + _filter_form_post_fields

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _filter_form_post_fields})]
    autocomplete_fields = ['user']

_whatsapp_lead_author_click_admin = ['lead', 'contactor', 'access_count']
@admin.register(models.WhatsAppLeadAuthorClick)
class WhatsAppLeadAuthorClickAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + \
        _whatsapp_lead_author_click_admin
    list_editable = comadm.standard_list_editable + \
        _whatsapp_lead_author_click_admin
    search_fields = comadm.standard_search_fields + \
        _whatsapp_lead_author_click_admin

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _whatsapp_lead_author_click_admin})]
    autocomplete_fields = ['lead', 'contactor']