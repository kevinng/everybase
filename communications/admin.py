from django.contrib import admin

from .models import Message, Recipient

class RecipientInline(admin.StackedInline):
    model = Recipient
    extra = 3

class MessageAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created')
    fieldsets = [
        (None, {'fields': ['sender', 'organization', 'comments', 'documents']}),
        ('Timestamps', {'fields': ['sent', 'created']}),
    ]
    inlines = [RecipientInline]

class RecipientAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    fieldsets = [
        (None, {'fields': ['email', 'account', 'organization', 'message']})
    ]

admin.site.register(Message, MessageAdmin)
admin.site.register(Recipient, RecipientAdmin)