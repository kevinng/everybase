from django.contrib import admin

from .models import (
    Document, DocumentType, File, DocumentMaterial, DocumentBatch,
    CreateFilePresignedURL, ReadFilePresignedURL)

admin.site.register(Document)
admin.site.register(DocumentType)
admin.site.register(File)
admin.site.register(DocumentMaterial)
admin.site.register(DocumentBatch)
admin.site.register(CreateFilePresignedURL)
admin.site.register(ReadFilePresignedURL)