from everybase.settings import BASE_URL
from urllib.parse import urljoin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib import admin
from files import models
from common import admin as comadm

_file_fields = ['uuid', 'file_url', 'uploader', 'file_type',
    'presigned_url_issued', 'presigned_url_lifespan', 'presigned_url_response',
    's3_bucket_name', 's3_object_key', 's3_object_content_length',
    's3_object_e_tag', 's3_object_content_type', 's3_object_last_modified']
@admin.register(models.File)
class FileAdmin(admin.ModelAdmin):
    def file_url(self, obj):
        url = urljoin(
            BASE_URL, reverse('files:get_file', args=[obj.id]))
        return format_html(f'<a href="{url}" target="{url}">{url}</a>')

    # List page settings
    list_display = comadm.standard_list_display + _file_fields
    list_editable = comadm.standard_list_editable + [
        's3_bucket_name', 's3_object_key', 's3_object_content_length',
        's3_object_e_tag', 's3_object_content_type', 's3_object_last_modified']
    list_filter = comadm.standard_list_filter + ['s3_object_last_modified']
    search_fields = ['id', 's3_bucket_name', 's3_object_key', 's3_object_e_tag']
    list_per_page = 50
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields + ['uuid', 'file_url']
    fieldsets = comadm.standard_fieldsets + [(None, {'fields': _file_fields})]