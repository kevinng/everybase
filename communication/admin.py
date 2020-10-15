from django.contrib import admin
from common.admin import (standard_fieldsets, standard_readonly_fields,
    ChoiceAdmin, ParentChildrenChoiceAdmin)
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

@admin.register(ConversationChannel, ConversationChatStatus,
    ConversationEmailStatus, ConversationVideoStatus, ConversationVoiceStatus)
class ChoiceAdmin(ChoiceAdmin):
    pass

# @admin.register(IssueStatus, IssueTag)
@admin.register(IssueTag)
class ParentChildrenChoiceAdmin(ParentChildrenChoiceAdmin):
    pass

admin.site.register(Issue)
admin.site.register(ConversationEmail)
admin.site.register(ConversationVoice)
admin.site.register(ConversationVideo)