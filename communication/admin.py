from django.contrib import admin
from common.admin import standard_fieldsets, standard_readonly_fields
from .models import (Issue, IssueTag, IssueStatus, Conversation,
    ConversationChannel, ConversationEmail, ConversationEmailStatus,
    ConversationChat, ConversationChatStatus, ConversationVoice,
    ConversationVoiceStatus, ConversationVideo, ConversationVideoStatus)

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    search_fields = ['id']

@admin.register(ConversationChat)
class ConversationChatAdmin(admin.ModelAdmin):
    # List page settings
    list_display = ['id', 'created', 'updated', 'status', 'our_number',
        'their_number', 'conversation']
    list_editable = ['status', 'our_number', 'their_number', 'conversation'] 
    list_filter = ['status']
    list_per_page = 1000
    search_fields = ['their_number', 'our_number', 'conversation']
    ordering = ['-created', '-updated']
    show_full_result_count = True
    
    # Details page settings
    save_on_top = True
    autocomplete_fields = ['status', 'their_number', 'our_number',
        'conversation']
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

@admin.register(ConversationChatStatus)
class ConversationChatStatusAdmin(admin.ModelAdmin):
    search_fields = ['id']

@admin.register(ConversationChannel)
class ConversationChannelAdmin(admin.ModelAdmin):
    # List page settings
    list_display = ['id', 'details_in_markdown', 'programmatic_key']
    search_fields = ['id', 'details_md', 'programmatic_key',
        'programmatic_details_md']

    def details_in_markdown(self, obj):
        return obj.details_md[0:15] + '...'
    details_in_markdown.empty_value_display = 'No Details'

admin.site.register(Issue)
admin.site.register(IssueTag)
admin.site.register(IssueStatus)
admin.site.register(ConversationEmail)
admin.site.register(ConversationEmailStatus)
admin.site.register(ConversationVoice)
admin.site.register(ConversationVoiceStatus)
admin.site.register(ConversationVideo)
admin.site.register(ConversationVideoStatus)