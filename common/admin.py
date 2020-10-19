from django.contrib import admin
from common.models import short_text, Country, State

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
choice_list_display = ['id', 'name', 'details_md', 'programmatic_key',
    'programmatic_details_md']
choice_list_editable = ['name', 'details_md', 'programmatic_key',
    'programmatic_details_md']

@admin.register(Country, State)
class ChoiceAdmin(admin.ModelAdmin):
    # List page settings
    list_display = choice_list_display
    list_editable = choice_list_editable
    list_per_page = 1000
    search_fields = ['id', 'details_md', 'programmatic_key',
        'programmatic_details_md']
    ordering = ['id']
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = choice_readonly_fields
    fieldsets = choice_fieldsets

class ParentChildrenChoiceAdmin(ChoiceAdmin):
    list_display = choice_list_display + ['parent']
    list_editable = choice_list_editable + ['parent']
    fieldsets = choice_fieldsets + [
        ('Relationship', {'fields': ['parent']})
    ]
    autocomplete_fields = ['parent']