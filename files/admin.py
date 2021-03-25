from django.contrib import admin
from . import models as mod
from common import admin as comadm

@admin.register(mod.File)
class FileAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['uuid', 'upload_confirmed',
        's3_bucket_name', 's3_object_key', 's3_object_content_length',
        's3_object_e_tag', 's3_object_content_type', 's3_object_last_modified']
    list_editable = comadm.standard_list_editable + ['upload_confirmed',
        's3_bucket_name', 's3_object_key', 's3_object_content_length',
        's3_object_e_tag', 's3_object_content_type', 's3_object_last_modified']
    list_filter = comadm.standard_list_filter + ['upload_confirmed',
        's3_object_last_modified']
    search_fields = ['id', 's3_bucket_name', 's3_object_key',
        's3_object_e_tag']
    list_per_page = 50
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields + ['uuid']
    fieldsets = comadm.standard_fieldsets + [
        (None, {
            'fields': ['upload_confirmed', 's3_bucket_name', 's3_object_key',
                's3_object_content_length', 's3_object_e_tag',
                's3_object_content_type', 's3_object_last_modified']
        })
    ]