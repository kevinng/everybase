from django.contrib import admin

class ChoiceAdmin(admin.ModelAdmin):
    """
    Choice admin definition to be inherited by child Choice models.
    """
    readonly_fields = ('id',)
    fieldsets = [
        (None, {'fields': ['id', 'name', 'details_md']}),
        ('Developer', {'fields': ['programmatic_key', 'programmatic_details_md']}),
    ]