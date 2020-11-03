from django.contrib import admin
from .models import FileTag, File
from common.admin import (standard_list_display, standard_list_filter,
    standard_ordering, standard_readonly_fields, standard_fieldsets,
    standard_list_editable, ParentChildrenChoiceAdmin)

@admin.register(FileTag)
class FileTagAdmin(ParentChildrenChoiceAdmin):
    pass

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    # List page settings
    list_display = standard_list_display + ['uuid', 'upload_confirmed',
        's3_bucket_name', 's3_object_key', 's3_object_content_length',
        's3_object_e_tag', 's3_object_content_type', 's3_object_last_modified',
        'details_md']
    list_editable = standard_list_editable + ['upload_confirmed',
        's3_bucket_name', 's3_object_key', 's3_object_content_length',
        's3_object_e_tag', 's3_object_content_type', 's3_object_last_modified',
        'details_md']
    list_filter = standard_list_filter + ['upload_confirmed',
        's3_object_last_modified']
    search_fields = ['id', 'uuid', 's3_bucket_name', 's3_object_key',
        's3_object_e_tag', 'tags']
    list_per_page = 1000
    ordering = standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = standard_readonly_fields + ['uuid']
    fieldsets = standard_fieldsets + [
        ('Details', {
            'fields': ['s3_bucket_name', 's3_object_key',
                's3_object_content_length', 's3_object_e_tag',
                's3_object_content_type', 's3_object_last_modified',
                'details_md', 'tags']
        })
    ]
    autocomplete_fields = ['tags']