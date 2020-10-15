from django.contrib import admin
from common.models import short_text

# Fields for standard models

standard_readonly_fields = ('id', 'created', 'updated')
standard_fieldsets = [
    (None, {'fields': ['id']}),
    ('Timestamps', {'fields': ['created', 'updated', 'deleted']})
]

# Fields for choice models

choice_readonly_fields = ('id',)
choice_fieldsets = [
    (None, {'fields': ['id', 'name', 'details_md']}),
    ('Developer', {'fields': [
        'programmatic_key',
        'programmatic_details_md']}),
]

class ChoiceAdmin(admin.ModelAdmin):
    # List page settings
    list_display = ['id', 'details_in_markdown', 'programmatic_key',
        'programmatic_details_in_markdown']
    list_editable = ['programmatic_key']
    list_per_page = 1000
    search_fields = ['id', 'details_md', 'programmatic_key',
        'programmatic_details_md']
    ordering = ['id']
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = choice_readonly_fields
    fieldsets = choice_fieldsets

    def details_in_markdown(self, obj):
        return short_text(obj.details_md)

    def programmatic_details_in_markdown(self, obj):
        return short_text(obj.programmatic_details_md)

class ParentChildrenChoice(admin.ModelAdmin):
    """
    Admin interface to be inherited by child of Choice model.
    """
    readonly_fields = ('id',)
    fieldsets = [
        (None, {'fields': ['id', 'name', 'details_md']}),
        ('Relationship', {'fields': ['parent']}),
        ('Developer', {'fields': [
                'programmatic_key',
                'programmatic_details_md']}),
    ]