from django.contrib import admin
from common import admin as comadm
from leads import models

_lead_fields = ['uuid', 'author', 'lead_type', 'author_type', 'title',
    'details', 'country_string', 'country', 'commission_pct',
    'commission_payable_after', 'other_commission_details']
@admin.register(models.Lead)
class LeadAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _lead_fields
    list_editable = comadm.standard_list_editable + _lead_fields
    list_filter = comadm.standard_list_filter + ['lead_type', 'author_type',
        'country', 'commission_payable_after']
    search_fields = comadm.standard_search_fields + ['title', 'details',
        'other_commission_details']

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
        [('Details', {'fields': _saved_lead_fields})]
    autocomplete_fields = ['lead', 'accessor']

_contact_request_fields = ['requested', 'responded', 'response', 'requester',
    'requestee', 'lead', 'message', 'access_count']
@admin.register(models.ContactRequest)
class ContactRequestAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _contact_request_fields
    list_editable = comadm.standard_list_editable + _contact_request_fields
    list_filter = comadm.standard_list_filter + ['requested', 'responded']
    search_fields = comadm.standard_search_fields + ['requester__first_name',
        'requester__last_name', 'requestee__first_name', 'requestee__last_name']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _saved_lead_fields})]
    autocomplete_fields = ['requester', 'requestee', 'lead']