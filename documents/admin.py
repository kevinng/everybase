from django.contrib import admin

from .models import (
    Document, DocumentType, File)

class DocumentAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created', 'updated')
    fieldsets = [
        (None, {'fields': ['id', 'creator', 'document_type', 'organization', 'batch', 'material']}),
        ('Timestamps', {'fields': ['created', 'updated', 'deleted']}),
    ]

class DocumentTypeAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    fieldsets = [
        (None, {'fields': ['id', 'name', 'acronym', 'level']})
    ]

admin.site.register(Document, DocumentAdmin)
admin.site.register(DocumentType, DocumentTypeAdmin)
admin.site.register(File)