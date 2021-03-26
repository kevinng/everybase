from django.contrib import admin
from common import models

# Fields for standard models

standard_list_display = ['id', 'created', 'updated', 'deleted']
standard_readonly_fields = ['id', 'created', 'updated']
standard_fieldsets = [
    (None, {'fields': ['id']}),
    ('Timestamps', {'fields': ['created', 'updated', 'deleted']})
]
standard_ordering = ['-created', '-updated']
standard_list_filter = ['created', 'updated', 'deleted']
standard_list_editable = ['deleted']

# Fields for choice models

choice_readonly_fields = ('id',)
choice_fieldsets = [
    (None, {'fields': ['id', 'name', 'description']}),
    ('Developer', {'fields': [
        'programmatic_key',
        'programmatic_details']}),
]
choice_list_display = ['id', 'name', 'programmatic_key', 'short_description',
    'short_programmatic_details']
choice_list_editable = ['name', 'programmatic_key']
choice_search_fields = ['id', 'name', 'programmatic_key', 'description',
    'programmatic_details']
choice_ordering = ['id']

class ChoiceAdmin(admin.ModelAdmin):
    # List page settings
    list_display = choice_list_display
    list_editable = choice_list_editable
    list_per_page = 50
    search_fields = choice_search_fields
    ordering = choice_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = choice_readonly_fields
    fieldsets = choice_fieldsets

    def short_description(self, obj):
        return models.short_text(obj.description)

    def short_programmatic_details(self, obj):
        return models.short_text(obj.programmatic_details)

@admin.register(models.State)
class StateAdmin(ChoiceAdmin):
    fieldsets = choice_fieldsets + [
        (None, {'fields': ['country', 'china_province_name_cn']})
    ]
    autocomplete_fields = ['country']

class ParentChildrenChoiceAdmin(ChoiceAdmin):
    list_display = choice_list_display + ['parent']
    list_editable = choice_list_editable + ['parent']
    fieldsets = choice_fieldsets + [
        ('Relationship', {'fields': ['parent']})
    ]
    autocomplete_fields = ['parent']

@admin.register(models.Country)
class CountryAdmin(ChoiceAdmin):
    list_display = choice_list_display + ['cc_tld']
    list_editable = choice_list_editable + ['cc_tld']
    search_fields = choice_search_fields + ['cc_tld']
    fieldsets = choice_fieldsets + [
        ('Other details', {'fields': ['cc_tld']})
    ]

@admin.register(models.Language)
class LanguageAdmin(ChoiceAdmin):
    pass

@admin.register(models.ImportJob)
class ImportJobAdmin(admin.ModelAdmin):
    # List page settings
    list_display = standard_list_display + ['status', 'description']
    list_editable = standard_list_editable + ['status', 'description']
    list_per_page = 50
    search_fields = ['id', 'status', 'description']
    list_filter = standard_list_filter + ['status', 'description']
    ordering = standard_ordering
    show_full_result_count = True

    # Details page settings
    readonly_fields = ['id', 'created', 'updated']
    fieldsets = standard_fieldsets + [
        (None, {'fields': ['status', 'description']})]

@admin.register(models.SystemTimestamp)
class SystemTimestampAdmin(admin.ModelAdmin):
    # List page settings
    list_display = standard_list_display + ['key', 'timestamp']
    list_editable = standard_list_editable
    list_per_page = 50
    search_fields = ['id', 'key', 'timestamp']
    list_filter = ['key'] + standard_list_filter
    ordering = standard_ordering
    show_full_result_count = True

    # Details page settings
    readonly_fields = standard_readonly_fields
    fieldsets = standard_fieldsets + [
        (None, {'fields': ['key', 'timestamp']})]