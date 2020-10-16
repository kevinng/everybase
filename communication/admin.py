from django.contrib import admin
from common.admin import (standard_readonly_fields, standard_fieldsets,
    ChoiceAdmin, ParentChildrenChoiceAdmin, short_text, standard_ordering)
from .models import (Issue, IssueTag, IssueStatus, Conversation,
    ConversationChannel, ConversationEmail, ConversationEmailStatus,
    ConversationChat, ConversationChatStatus, ConversationVoice,
    ConversationVoiceStatus, ConversationVideo, ConversationVideoStatus)

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    # List page settings
    list_display = ['id', 'created', 'updated', 'deleted', 'channel',
        'agenda_md', 'minutes_md', 'front_conversation_id', 'issue']
    list_editable = ['deleted', 'agenda_md', 'channel',
        'minutes_md', 'front_conversation_id', 'issue']
    list_filter = ['channel']
    search_fields = ['id', 'agenda_md', 'minutes_md', 'front_conversation_id',
        'issue']
    list_per_page = 1000
    ordering = standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = standard_readonly_fields
    fieldsets = standard_fieldsets + [
        ('Channel', {
            'fields': ['channel']
        }),
        (None, {
            'fields': ['emails', 'chats', 'voices', 'videos'],
            'description': 'One of the following channels must be set'
        }),
        ('Details', {
            'fields': ['front_conversation_id', 'agenda_md', 'minutes_md',
                'issue']
        })
    ]
    autocomplete_fields = ['channel', 'emails', 'chats', 'voices', 'videos',
        'issue']

@admin.register(ConversationChat)
class ConversationChatAdmin(admin.ModelAdmin):
    # List page settings
    list_display = ['id', 'created', 'updated', 'deleted', 'status',
        'our_number', 'their_number', 'conversation']
    list_editable = ['status', 'deleted', 'our_number', 'their_number',
        'conversation'] 
    list_per_page = 1000
    list_filter = ['status']
    search_fields = ['id', 'their_number', 'our_number', 'conversation']
    ordering = standard_ordering
    show_full_result_count = True
    
    # Details page settings
    save_on_top = True
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
    autocomplete_fields = ['status', 'their_number', 'our_number',
        'conversation']

@admin.register(ConversationEmail)
class ConversationEmailAdmin(admin.ModelAdmin):
    # List page settings
    list_display = ['id', 'created', 'updated', 'deleted', 'status',
        'our_email', 'their_email', 'conversation']
    list_editable = ['status', 'deleted', 'our_email', 'their_email',
        'conversation']
    list_per_page = 1000
    list_filter = ['status']
    search_fields = ['id', 'our_email', 'their_email', 'conversation']
    ordering = standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = standard_readonly_fields
    fieldsets = standard_fieldsets + [
        ('Basic Details', {'fields': ['status']}),
        ('Emails', {
            'fields': ['their_email', 'our_email'],
            'description': 'Emails involved in this conversation'
        }),
        ('Conversation', {
            'fields': ['conversation'],
            'description': 'Base conversation'
        })
    ]
    autocomplete_fields = ['status', 'their_email', 'our_email', 'conversation']

@admin.register(ConversationVoice)
class ConversationVoiceAdmin(admin.ModelAdmin):
    search_fields = ['id']
    ordering = standard_ordering

@admin.register(ConversationVideo)
class ConversationVideoAdmin(admin.ModelAdmin):
    search_fields = ['id']
    ordering = standard_ordering

@admin.register(ConversationChannel, ConversationChatStatus,
    ConversationEmailStatus, ConversationVideoStatus, ConversationVoiceStatus)
class ChoiceAdmin(ChoiceAdmin):
    pass

@admin.register(IssueStatus, IssueTag)
class ParentChildrenChoiceAdmin(ParentChildrenChoiceAdmin):
    pass

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    # List page settings
    list_display = ['id', 'status', 'scheduled', 'source_type', 'tags_string',
        'description_md', 'outcome_md']
    list_editable = ['status', 'scheduled', 'description_md', 'outcome_md']
    list_per_page = 1000
    list_filter = ['status', 'tags']
    search_fields = ['id', 'description_md', 'outcome_md']
    ordering = standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
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
            'description': 'Source of this issue - at least one of these must \
                be set'
        })
    ]
    autocomplete_fields = ['status', 'tags', 'supply', 'demand', 'supply_quote',
        'match', 'supply_commission', 'demand_commission']

    def source_type(self, obj):
        if obj.supply is not None:
            return 'Supply'
        elif obj.demand is not None:
            return 'Demand'
        elif obj.supply_quote is not None:
            return 'Supply Quote'
        elif obj.match is not None:
            return 'Match'
        elif obj.supply_commission is not None:
            return 'Supply Commission'
        elif obj.demand_commission is not None:
            return 'Demand Commission'
        
        return '-'
    
    def tags_string(self, obj):
        return ', '.join([t.name for t in obj.tags.all()])