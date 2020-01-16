from django.contrib import admin

from .models import Material, Batch

class MaterialAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created', 'updated')
    fieldsets = [
        (None, {'fields': ['id', 'name', 'code', 'organization']}),
        ('Timestamps', {'fields': ['created', 'updated', 'deleted']}),
    ]

class BatchAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created', 'updated')
    fieldsets = [
        (None, {'fields': ['id', 'code', 'material']}),
        ('Timestamps', {'fields': ['created', 'updated', 'deleted']}),
    ]

admin.site.register(Material, MaterialAdmin)
admin.site.register(Batch, BatchAdmin)