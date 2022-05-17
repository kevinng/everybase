from everybase.settings import MEDIA_URL, AWS_S3_KEY_LEAD_IMAGE, AWS_S3_KEY_LEAD_IMAGE_THUMBNAIL
from urllib.parse import urljoin
from django.utils.html import format_html
from django.contrib import admin
from files import models
from common import admin as comadm

_file_fields = ['uploader', 'mime_type', 'filename', 'presigned_url_issued',
    'presigned_url_lifespan', 'presigned_url_response', 's3_bucket_name',
    's3_object_key', 'width', 'height', 'thumbnail_s3_bucket_name',
    'thumbnail_s3_object_key', 'thumbnail_width', 'thumbnail_height',
    's3_object_content_length', 's3_object_e_tag', 's3_object_content_type',
    's3_object_last_modified', 'lead']
@admin.register(models.File)
class FileAdmin(comadm.StandardAdmin):
    def lead_image_url(self, obj):
        if obj.lead is None:
            return 'Not a lead image'

        path = AWS_S3_KEY_LEAD_IMAGE % (obj.lead.id, obj.id)
        url = urljoin(MEDIA_URL, path)
        return format_html(f'<a href="{url}" target="{url}">{url}</a>')

    def lead_thumb_url(self, obj):
        if obj.lead is None:
            return 'Not a lead image'

        path = AWS_S3_KEY_LEAD_IMAGE_THUMBNAIL % (obj.lead.id, obj.id)
        url = urljoin(MEDIA_URL, path)
        return format_html(f'<a href="{url}" target="{url}">{url}</a>')

    # List page settings
    list_display = comadm.standard_list_display + _file_fields + ['uuid',
        'lead_image_url', 'lead_thumb_url']
    list_editable = comadm.standard_list_editable + _file_fields
    list_filter = comadm.standard_list_filter + ['mime_type',
        'presigned_url_issued']
    search_fields = ['id', 'uuid', 'mime_type', 'filename', 's3_bucket_name',
        's3_object_key', 'thumbnail_s3_bucket_name', 'thumbnail_s3_object_key',
        'lead__headline', 'lead__id']
    list_per_page = 50
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields + ['uuid',
        'lead_image_url', 'lead_thumb_url']
    fieldsets = comadm.standard_fieldsets + [(None, {'fields': _file_fields +\
        ['uuid', 'lead_image_url', 'lead_thumb_url']})]
    autocomplete_fields = ['uploader', 'lead']

class FileInlineAdmin(admin.TabularInline):
    model = models.File
    extra = 1
    fields = ['uploader', 'mime_type', 'filename', 'presigned_url_issued',
        'presigned_url_lifespan', 'presigned_url_response', 's3_bucket_name',
        's3_object_key', 'thumbnail_s3_bucket_name', 'thumbnail_s3_object_key',
        's3_object_content_length', 's3_object_e_tag', 's3_object_content_type',
        's3_object_last_modified', 'lead'] + ['uuid', 'lead_image_url',
        'lead_thumb_url']
    readonly_fields = ['uuid', 'lead_image_url', 'lead_thumb_url']

    def lead_image_url(self, obj):
        if obj.lead is None:
            return 'Not a lead image'

        path = AWS_S3_KEY_LEAD_IMAGE % (obj.lead.id, obj.id)
        url = urljoin(MEDIA_URL, path)
        return format_html(f'<a href="{url}" target="{url}">{url}</a>')

    def lead_thumb_url(self, obj):
        if obj.lead is None:
            return 'Not a lead image'

        path = AWS_S3_KEY_LEAD_IMAGE_THUMBNAIL % (obj.lead.id, obj.id)
        url = urljoin(MEDIA_URL, path)
        return format_html(f'<a href="{url}" target="{url}">{url}</a>')