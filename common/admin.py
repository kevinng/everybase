from django.contrib import admin
from common.models import short_text, Country, State, ImportJob

# Fields for standard models

standard_list_display = ['id', 'created', 'updated', 'deleted']
standard_readonly_fields = ['id', 'created', 'updated']
standard_fieldsets = [
    (None, {'fields': ['id']}),
    ('Timestamps', {'fields': ['created', 'updated', 'deleted']})
]
standard_ordering = ['-created', '-updated']
standard_list_filter = ['updated', 'deleted']
standard_list_editable = ['deleted']

# Fields for choice models

choice_readonly_fields = ('id',)
choice_fieldsets = [
    (None, {'fields': ['id', 'name', 'details_md']}),
    ('Developer', {'fields': [
        'programmatic_key',
        'programmatic_details_md']}),
]
choice_list_display = ['id', 'name', 'programmatic_key', 'short_details_md',
    'short_programmatic_details_md']
choice_list_editable = ['name', 'programmatic_key']
choice_search_fields = ['id', 'name', 'programmatic_key', 'details_md',
    'programmatic_details_md']
choice_ordering = ['id']

@admin.register(State)
class ChoiceAdmin(admin.ModelAdmin):
    # List page settings
    list_display = choice_list_display
    list_editable = choice_list_editable
    list_per_page = 1000
    search_fields = choice_search_fields
    ordering = choice_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = choice_readonly_fields
    fieldsets = choice_fieldsets

    def short_details_md(self, obj):
        return short_text(obj.details_md)

    def short_programmatic_details_md(self, obj):
        return short_text(obj.programmatic_details_md)

class ParentChildrenChoiceAdmin(ChoiceAdmin):
    list_display = choice_list_display + ['parent']
    list_editable = choice_list_editable + ['parent']
    fieldsets = choice_fieldsets + [
        ('Relationship', {'fields': ['parent']})
    ]
    autocomplete_fields = ['parent']

@admin.register(Country)
class CountryAdmin(ChoiceAdmin):
    list_display = choice_list_display + ['cc_tld']
    list_editable = choice_list_editable + ['cc_tld']
    search_fields = choice_search_fields + ['cc_tld']
    fieldsets = choice_fieldsets + [
        ('Other details', {'fields': ['cc_tld']})
    ]

@admin.register(ImportJob)
class ImportJobAdmin(admin.ModelAdmin):
    # List page settings
    list_display = standard_list_display + ['started', 'ended', 'status']
    list_editable = standard_list_editable + ['started', 'ended', 'status']
    list_per_page = 1000
    list_filter = standard_list_filter + ['started', 'ended', 'status']
    ordering = standard_ordering
    show_full_result_count = True

    # Details page settings
    readonly_fields = ['id', 'created', 'updated']
    fieldsets = standard_fieldsets + [
        (None, {'fields': ['started', 'ended', 'status']})]