from django.contrib import admin

class StandardAdmin(admin.ModelAdmin):
    """
    Admin interface to be inherited by child of Standard model.
    """
    readonly_fields = ('id',)
    fieldsets = [
        (None, {'fields': ['id', 'created']}),
        ('Timestamps', {'fields': ['updated', 'deleted']})
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