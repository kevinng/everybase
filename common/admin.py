from django.contrib import admin

# Fields for standard models

standard_readonly_fields = ('id', 'created', 'updated')
standard_fieldsets = [
    (None, {'fields': ['id']}),
    ('Timestamps', {'fields': ['created', 'updated', 'deleted']})
]

class ChoiceAdmin(admin.ModelAdmin):
    """
    Admin interface to be inherited by child of Choice.
    """
    readonly_fields = ('id',)
    fieldsets = [
        (None, {'fields': ['id', 'name', 'details_md']}),
        ('Developer', {'fields': [
            'programmatic_key',
            'programmatic_details_md']}),
    ]

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