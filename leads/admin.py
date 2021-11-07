from django.contrib import admin
from common import admin as comadm
from leads import models

_lead_fields = ['author', 'lead_type', 'author_type', 'title', 'details',
    'country_string', 'country', 'commission_pct', 'commission_payable_after',
    'other_commission_details']
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
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _lead_fields})]
    autocomplete_fields = ['author', 'country']

_lead_document_fields = ['lead', 'file']
@admin.register(models.LeadDocument)
class LeadDocumentAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _lead_document_fields
    list_editable = comadm.standard_list_editable + _lead_document_fields
    search_fields = comadm.standard_search_fields + ['lead__id', 'lead__title',
        'lead__description']

    # Details page settings
    readonly_fields = comadm.standard_readonly_fields + ['id']
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _lead_document_fields})]
    autocomplete_fields = ['lead', 'file']

_lead_image_fields = ['lead', 'file']
@admin.register(models.LeadImage)
class LeadImageAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _lead_image_fields
    list_editable = comadm.standard_list_editable + _lead_image_fields
    search_fields = comadm.standard_search_fields + ['lead__id', 'lead__title',
        'lead__description']

    # Details page settings
    readonly_fields = comadm.standard_readonly_fields + ['id']
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _lead_image_fields})]
    autocomplete_fields = ['lead', 'file']

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