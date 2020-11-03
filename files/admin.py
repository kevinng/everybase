from django.contrib import admin
from . import models as mod
from common import admin as comadm

@admin.register(mod.FileTag)
class FileTagAdmin(comadm.ParentChildrenChoiceAdmin):
    pass

@admin.register(mod.File)
class FileAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['upload_confirmed',
        's3_bucket_name', 's3_object_key', 's3_object_content_length',
        's3_object_e_tag', 's3_object_content_type', 's3_object_last_modified',
        'details_md']
    list_editable = comadm.standard_list_editable + ['upload_confirmed',
        's3_bucket_name', 's3_object_key', 's3_object_content_length',
        's3_object_e_tag', 's3_object_content_type', 's3_object_last_modified',
        'details_md']
    list_filter = comadm.standard_list_filter + ['upload_confirmed',
        's3_object_last_modified']
    search_fields = ['id', 's3_bucket_name', 's3_object_key',
        's3_object_e_tag', 'tags']
    list_per_page = 1000
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {
            'fields': ['s3_bucket_name', 's3_object_key',
                's3_object_content_length', 's3_object_e_tag',
                's3_object_content_type', 's3_object_last_modified',
                'details_md', 'tags']
        })
    ]
    autocomplete_fields = ['tags']

# --- Start: Relationships ---

@admin.register(
    mod.FileSupplyType,
    mod.FileDemandType,
    mod.FileIssueType,
    mod.FilePersonType)
class ChoiceAdmin(comadm.ChoiceAdmin):
    """
    Relationship-type class admin definition.
    """
    pass

_rel_list_display = comadm.standard_list_display + \
    ['details_md', 'rtype', 'file']
_rel_list_editable = comadm.standard_list_editable + \
    ['details_md', 'rtype', 'file']
_rel_list_search_fields = ['id', 'details_md', 'rtype', 'file']
_rel_fieldsets = comadm.standard_fieldsets + \
    [(None, {'fields': ['details_md', 'rtype', 'file']})]
_rel_autocomplete = ['rtype', 'file']

class RelationshipAdmin(admin.ModelAdmin):
    """
    Abstract admin definition class for file relationships.
    """
    # List page settings
    list_per_page = 1000
    list_filter = comadm.standard_list_filter
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields

@admin.register(mod.FileSupply)
class FileSupplyAdmin(RelationshipAdmin):
    # List page settings
    list_display = _rel_list_display + ['supply']
    list_editable = _rel_list_editable + ['supply']
    search_fields = _rel_list_search_fields + ['supply']

    # Details page settings
    fieldsets = _rel_fieldsets + [(None, {'fields': ['supply']})]
    autocomplete_fields = _rel_autocomplete + ['supply']

@admin.register(mod.FileDemand)
class FileDemandAdmin(RelationshipAdmin):
    # List page settings
    list_display = _rel_list_display + ['demand']
    list_editable = _rel_list_editable + ['demand']
    search_fields = _rel_list_search_fields + ['demand']

    # Details page settings
    fieldsets = _rel_fieldsets + [(None, {'fields': ['demand']})]
    autocomplete_fields = _rel_autocomplete + ['demand']

@admin.register(mod.FileIssue)
class FileIssueAdmin(RelationshipAdmin):
    # List page settings
    list_display = _rel_list_display + ['issue']
    list_editable = _rel_list_editable + ['issue']
    search_fields = _rel_list_search_fields + ['issue']

    # Details page settings
    fieldsets = _rel_fieldsets + [(None, {'fields': ['issue']})]
    autocomplete_fields = _rel_autocomplete + ['issue']

@admin.register(mod.FilePerson)
class FilePersonAdmin(RelationshipAdmin):
    # List page settings
    list_display = _rel_list_display + ['person']
    list_editable = _rel_list_editable + ['person']
    search_fields = _rel_list_search_fields + ['person']

    # Details page settings
    fieldsets = _rel_fieldsets + [(None, {'fields': ['person']})]
    autocomplete_fields = _rel_autocomplete + ['person']

# --- End: Relationships ---