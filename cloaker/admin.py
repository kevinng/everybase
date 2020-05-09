from django.contrib import admin

from .models import CloakedLink

class CloakedLinkAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    fieldsets = [
        (None, {'fields': ['id']}),
        ('Details', {'fields': ['page_title', 'description', 'url', 'redirect']}),
    ]

admin.site.register(CloakedLink, CloakedLinkAdmin)