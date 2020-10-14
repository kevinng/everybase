from django.contrib import admin
from common.admin import standard_fieldsets, standard_readonly_fields
from .models import (Issue, IssueTag, IssueStatus, Conversation,
    ConversationChannel, ConversationEmail, ConversationEmailStatus,
    ConversationChat, ConversationChatStatus, ConversationVoice,
    ConversationVoiceStatus, ConversationVideo, ConversationVideoStatus)


class ConversationChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'their_number')
    readonly_fields = standard_readonly_fields
    fieldsets = standard_fieldsets + [
        ('Basic Details', {'fields': ['status']}),
        ('Phone Numbers', {
            'fields': ['their_number', 'our_number'],
            'description': 'Phone numbers involved in this chat conversation'
        }),
        ('Conversation', {
            'fields': ['conversation'],
            'description': 'Base conversation'
        })
    ]

admin.site.register(Issue)
admin.site.register(IssueTag)
admin.site.register(IssueStatus)
admin.site.register(Conversation)
admin.site.register(ConversationChannel)
admin.site.register(ConversationEmail)
admin.site.register(ConversationEmailStatus)
admin.site.register(ConversationChat, ConversationChatAdmin)
admin.site.register(ConversationChatStatus)
admin.site.register(ConversationVoice)
admin.site.register(ConversationVoiceStatus)
admin.site.register(ConversationVideo)
admin.site.register(ConversationVideoStatus)