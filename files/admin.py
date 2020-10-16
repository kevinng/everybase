from django.contrib import admin
from .models import FileTag, File
from common.admin import (standard_list_display, standard_list_filter,
    standard_ordering, standard_readonly_fields, standard_fieldsets,
    standard_list_editable, ChoiceAdmin)

@admin.register(FileTag)
class FileTagAdmin(ChoiceAdmin):
    pass

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    # List page settings
    list_display = standard_list_display + ['s3_url', 'details_md',
        'source_person', 'source_issue']
    list_editable = standard_list_editable + ['s3_url', 'details_md',
        'source_person', 'source_issue']
    list_filter = standard_list_filter + ['source_person', 'source_issue']
    search_fields = ['id', 's3_url', 'details_md', 'source_person',
        'source_issue']
    list_per_page = 1000
    ordering = standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = standard_readonly_fields
    fieldsets = standard_fieldsets + [
        ('Details', {
            'fields': ['s3_url', 'details_md', 'tags']
        }),
        ('Source', {
            'fields': ['source_person', 'source_issue']
        }),
        ('Anonymization', {
            'fields': ['anonymization_source']
        }),
    ]
    autocomplete_fields = ['tags', 'source_person', 'source_issue',
        'anonymization_source']