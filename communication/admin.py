from django.contrib import admin
from common.admin import (standard_readonly_fields, standard_fieldsets,
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

@admin.register(IssueStatus, IssueTag)
class ParentChildrenChoiceAdmin(ParentChildrenChoiceAdmin):
    pass

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    readonly_fields = standard_readonly_fields
    fieldsets = standard_fieldsets + [
        ('Schedule', {
            'fields': ['scheduled'],
            'description': 'Time scheduled to begin working on this issue'
        }),
        ('Notes', {
            'fields': ['description_md', 'outcome_md'],
            'description': 'Notes on this issue'
        }),
        ('Meta-Data', {
            'fields': ['status', 'tags']
        }),
        ('Source', {
            'fields': ['supply', 'demand', 'supply_quote', 'match',
                'supply_commission', 'demand_commission'],
            'description': 'Source of this issue - one of these must be set'
        })
    ]
    autocomplete_fields = ['status', 'tags', 'supply', 'demand', 'supply_quote',
        'match', 'supply_commission', 'demand_commission']


admin.site.register(ConversationEmail)
admin.site.register(ConversationVoice)
admin.site.register(ConversationVideo)