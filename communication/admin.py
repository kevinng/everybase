from django.contrib import admin
from . import models as mod
from common import admin as comadm

@admin.register(mod.Conversation)
class ConversationAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['channel', 'agenda_md',
        'minutes_md', 'front_conversation_id', 'issue']
    list_editable = comadm.standard_list_editable + ['agenda_md', 'channel',
        'minutes_md', 'front_conversation_id', 'issue']
    list_filter = comadm.standard_list_filter + ['channel']
    search_fields = ['id', 'agenda_md', 'minutes_md', 'front_conversation_id',
        'issue']
    list_per_page = 50
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': ['channel']}),
        (None, {'fields': ['emails', 'chats', 'voices', 'videos'],
            'description': 'One of the following channels must be set'}),
        (None, {'fields': ['front_conversation_id', 'agenda_md', 'minutes_md',
            'issue']})
    ]
    autocomplete_fields = ['channel', 'emails', 'chats', 'voices', 'videos',
        'issue']

@admin.register(mod.ConversationChat)
class ConversationChatAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['status', 'our_number',
        'their_number', 'conversation']
    list_editable = comadm.standard_list_editable + ['status', 'our_number',
        'their_number', 'conversation'] 
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['status']
    search_fields = ['id', 'their_number', 'our_number', 'conversation']
    ordering = comadm.standard_ordering
    show_full_result_count = True
    
    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': ['status', 'their_number', 'our_number',
            'conversation']})]
    autocomplete_fields = ['status', 'their_number', 'our_number',
        'conversation']

@admin.register(mod.ConversationEmail)
class ConversationEmailAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['status', 'our_email',
        'their_email', 'conversation']
    list_editable = comadm.standard_list_editable + ['status', 'our_email',
        'their_email', 'conversation']
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['status']
    search_fields = ['id', 'our_email', 'their_email', 'conversation']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': ['status']}),
        (None, {'fields': ['their_email', 'our_email', 'conversation']})]
    autocomplete_fields = ['status', 'their_email', 'our_email', 'conversation']

@admin.register(
    mod.ConversationVoice,
    mod.ConversationVideo)
class ConversationVoiceAndVideoAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['status', 'our_number',
        'their_number', 'conversation']
    list_editable = comadm.standard_list_editable + ['status', 'our_number',
        'their_number', 'conversation'] 
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['status']
    search_fields = ['id', 'their_number', 'our_number', 'conversation']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': ['status']}),
        (None, {'fields': ['their_number', 'our_number']}),
        (None, {'fields': ['conversation']})]
    autocomplete_fields = ['status', 'their_number', 'our_number',
        'conversation']

@admin.register(
    mod.ConversationChannel,
    mod.ConversationChatStatus,
    mod.ConversationEmailStatus,
    mod.ConversationVideoStatus,
    mod.ConversationVoiceStatus)
class ChoiceAdmin(comadm.ChoiceAdmin):
    pass

@admin.register(
    mod.IssueStatus,
    mod.IssueTag)
class ParentChildrenChoiceAdmin(comadm.ParentChildrenChoiceAdmin):
    pass

@admin.register(mod.Issue)
class IssueAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['status', 'scheduled',
        'source_type', 'tags_string', 'description_md', 'outcome_md']
    list_editable = comadm.standard_list_editable + ['status', 'scheduled',
        'description_md', 'outcome_md']
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['status', 'tags']
    search_fields = ['id', 'description_md', 'outcome_md']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': ['scheduled', 'description_md', 'outcome_md',
            'status', 'tags']}),
        ('Source', {
            'fields': ['supply', 'demand', 'supply_quote', 'match',
                'supply_commission', 'demand_commission'],
            'description': 'At least one of these sources must be set'})]
    autocomplete_fields = ['status', 'tags', 'supply', 'demand', 'supply_quote',
        'match', 'supply_commission', 'demand_commission', 'company', 'person']

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