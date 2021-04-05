# from django.contrib import admin
# from . import models as mod
# from common import admin as comadm

# # --- Start: Inline ---

# class ConversationInlineAdmin(admin.TabularInline):
#     model = mod.Conversation
#     extra = 1
#     autocomplete_fields = ['channel', 'emails', 'chats', 'voices', 'videos']

# # --- End: Inline ---

# @admin.register(mod.Conversation)
# class ConversationAdmin(admin.ModelAdmin):
#     # List page settings
#     list_display = comadm.standard_list_display + ['channel', 'agenda_md',
#         'minutes_md', 'issue']
#     list_editable = comadm.standard_list_editable + ['agenda_md', 'channel',
#         'minutes_md', 'issue']
#     list_filter = comadm.standard_list_filter + ['channel']
#     search_fields = ['id', 'agenda_md', 'minutes_md', 'front_conversation_id',
#         'issue']
#     list_per_page = 50
#     ordering = comadm.standard_ordering
#     show_full_result_count = True

#     # Details page settings
#     save_on_top = True
#     readonly_fields = comadm.standard_readonly_fields
#     fieldsets = comadm.standard_fieldsets + [
#         (None, {'fields': ['channel']}),
#         (None, {'fields': ['emails', 'chats', 'voices', 'videos'],
#             'description': 'One of the following channels must be set'}),
#         (None, {'fields': ['agenda_md', 'minutes_md', 'issue']})
#     ]
#     autocomplete_fields = ['channel', 'emails', 'chats', 'voices', 'videos',
#         'issue']

# @admin.register(mod.ConversationChat)
# class ConversationChatAdmin(admin.ModelAdmin):
#     # List page settings
#     list_display = comadm.standard_list_display + ['status', 'our_number',
#         'their_number', 'conversation']
#     list_editable = comadm.standard_list_editable + ['status', 'our_number',
#         'their_number', 'conversation'] 
#     list_per_page = 50
#     list_filter = comadm.standard_list_filter + ['status']
#     search_fields = ['id', 'their_number', 'our_number', 'conversation']
#     ordering = comadm.standard_ordering
#     show_full_result_count = True
    
#     # Details page settings
#     save_on_top = True
#     readonly_fields = comadm.standard_readonly_fields
#     fieldsets = comadm.standard_fieldsets + [
#         (None, {'fields': ['status', 'their_number', 'our_number',
#             'conversation']})]
#     autocomplete_fields = ['status', 'their_number', 'our_number',
#         'conversation']

# @admin.register(mod.ConversationEmail)
# class ConversationEmailAdmin(admin.ModelAdmin):
#     # List page settings
#     list_display = comadm.standard_list_display + ['status', 'our_email',
#         'their_email', 'conversation']
#     list_editable = comadm.standard_list_editable + ['status', 'our_email',
#         'their_email', 'conversation']
#     list_per_page = 50
#     list_filter = comadm.standard_list_filter + ['status']
#     search_fields = ['id', 'our_email', 'their_email', 'conversation']
#     ordering = comadm.standard_ordering
#     show_full_result_count = True

#     # Details page settings
#     save_on_top = True
#     readonly_fields = comadm.standard_readonly_fields
#     fieldsets = comadm.standard_fieldsets + [
#         (None, {'fields': ['status']}),
#         (None, {'fields': ['their_email', 'our_email', 'conversation']})]
#     autocomplete_fields = ['status', 'their_email', 'our_email', 'conversation']

# @admin.register(
#     mod.ConversationVoice,
#     mod.ConversationVideo)
# class ConversationVoiceAndVideoAdmin(admin.ModelAdmin):
#     # List page settings
#     list_display = comadm.standard_list_display + ['status', 'our_number',
#         'their_number', 'conversation']
#     list_editable = comadm.standard_list_editable + ['status', 'our_number',
#         'their_number', 'conversation'] 
#     list_per_page = 50
#     list_filter = comadm.standard_list_filter + ['status']
#     search_fields = ['id', 'their_number', 'our_number', 'conversation']
#     ordering = comadm.standard_ordering
#     show_full_result_count = True

#     # Details page settings
#     save_on_top = True
#     readonly_fields = comadm.standard_readonly_fields
#     fieldsets = comadm.standard_fieldsets + [
#         (None, {'fields': ['status']}),
#         (None, {'fields': ['their_number', 'our_number']}),
#         (None, {'fields': ['conversation']})]
#     autocomplete_fields = ['status', 'their_number', 'our_number',
#         'conversation']

# @admin.register(
#     mod.ConversationChannel,
#     mod.ConversationChatStatus,
#     mod.ConversationEmailStatus,
#     mod.ConversationVideoStatus,
#     mod.ConversationVoiceStatus)
# class ChoiceAdmin(comadm.ChoiceAdmin):
#     pass

# @admin.register(
#     mod.IssueStatus,
#     mod.IssueTag)
# class ParentChildrenChoiceAdmin(comadm.ParentChildrenChoiceAdmin):
#     pass

# _issue_related_fields = ['supply', 'demand', 'supply_quote', 'demand_quote',
#     'match', 'supply_commission', 'demand_commission', 'company', 'person']
# @admin.register(mod.Issue)
# class IssueAdmin(admin.ModelAdmin):
#     # List page settings
#     list_display = comadm.standard_list_display + _issue_related_fields + \
#         ['status', 'scheduled', 'tags_string', 'description_md', 'outcome_md']
#     list_editable = comadm.standard_list_editable + _issue_related_fields + \
#         ['status', 'scheduled', 'description_md', 'outcome_md']
#     list_per_page = 50
#     list_filter = comadm.standard_list_filter + ['status', 'tags']
#     search_fields = ['id', 'description_md', 'outcome_md']
#     ordering = comadm.standard_ordering
#     show_full_result_count = True

#     # Details page settings
#     save_on_top = True
#     readonly_fields = comadm.standard_readonly_fields
#     fieldsets = comadm.standard_fieldsets + [
#         ('Details', {'fields': ['scheduled', 'description_md', 'outcome_md',
#             'status', 'tags']}),
#         ('Related', {
#             'fields': _issue_related_fields})]
#     autocomplete_fields = ['status', 'tags'] + _issue_related_fields
#     inlines = [ConversationInlineAdmin]
    
#     def tags_string(self, obj):
#         return ', '.join([t.name for t in obj.tags.all()])