from django.contrib import admin
from common import admin as comadm
from leads import models

_lead_fields = ['closed', 'owner', 'lead_type', 'title', 'description',
    'is_buying', 'agent_sale_commission_pct', 'country']
@admin.register(models.Lead)
class LeadAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _lead_fields
    list_editable = comadm.standard_list_editable + _lead_fields
    list_filter = comadm.standard_list_filter + ['closed', 'lead_type',
        'is_buying']
    search_fields = comadm.standard_search_fields + ['owner__name', 'title',
        'description']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _lead_fields + ['tags']})]
    autocomplete_fields = ['owner', 'country', 'tags']

_lead_document_fields = ['uploaded', 'lead', 'file']
@admin.register(models.LeadDocument)
class LeadDocumentAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _lead_document_fields
    list_editable = comadm.standard_list_editable + _lead_document_fields
    list_filter = comadm.standard_list_filter + ['uploaded']
    search_fields = comadm.standard_search_fields + ['lead__id', 'lead__title',
        'lead__description']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _lead_document_fields})]
    autocomplete_fields = ['lead', 'file']

_lead_image_fields = ['uploaded', 'lead', 'file']
@admin.register(models.LeadImage)
class LeadImageAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _lead_image_fields
    list_editable = comadm.standard_list_editable + _lead_image_fields
    list_filter = comadm.standard_list_filter + ['uploaded']
    search_fields = comadm.standard_search_fields + ['lead__id', 'lead__title',
        'lead__description']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _lead_image_fields})]
    autocomplete_fields = ['lead', 'file']

_lead_tag_fields = ['tag', 'internal_notes']
@admin.register(models.LeadTag)
class LeadTagAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _lead_tag_fields
    list_editable = comadm.standard_list_editable + _lead_tag_fields
    search_fields = comadm.standard_search_fields + ['tag', 'internal_notes']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _lead_tag_fields})]


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