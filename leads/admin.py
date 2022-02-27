from django.contrib import admin
from common import admin as comadm
from files import admin as fiadm
from leads import models

_lead_fields = ['author', 'author_type', 'buy_country', 'sell_country',
    'lead_type', 'details', 'need_agent', 'commission_payable_by',
    'commission', 'commission_type', 'commission_type_other',
    'is_comm_negotiable', 'avg_deal_size', 'commission_payable_after',
    'commission_payable_after_other', 'other_agent_details',
    'need_logistics_agent', 'other_logistics_agent_details',
    
    'internal_notes', 'onboarding', 'onboarded',

    'saved_count', 'search_appearance_count', 'search_to_lead_details_count',
    'search_to_user_details_count',
    
    # Keep for future
    'title', 'country'
]
@admin.register(models.Lead)
class LeadAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['uuid'] + _lead_fields
    list_editable = comadm.standard_list_editable + _lead_fields
    list_filter = comadm.standard_list_filter + ['buy_country', 'sell_country',
        'lead_type', 'need_agent', 'commission_payable_by', 'commission_type',
        'is_comm_negotiable', 'commission_payable_after',
        'need_logistics_agent', 'onboarding', 'onboarded']
    search_fields = comadm.standard_search_fields + ['details',
        'other_agent_details', 'other_logistics_agent_details',
        'internal_notes']

    # Details page settings
    readonly_fields = comadm.standard_readonly_fields + ['uuid']
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _lead_fields})]
    autocomplete_fields = ['author', 'buy_country', 'sell_country']
    inlines = [fiadm.FileInlineAdmin]

_saved_lead_fields = ['saved', 'saver', 'lead']
@admin.register(models.SavedLead)
class SavedLeadAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _saved_lead_fields
    list_editable = comadm.standard_list_editable + _saved_lead_fields
    list_filter = comadm.standard_list_filter + ['saved']
    search_fields = comadm.standard_search_fields + ['saver__id',
        'saver__family_first_name', 'saver__family_last_name',
        'lead__id', 'lead__title', 'lead__description']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _saved_lead_fields})]
    autocomplete_fields = ['saver', 'lead']

_lead_detail_view_fields = ['lead', 'viewer', 'count']
@admin.register(models.LeadDetailView)
class LeadDetailViewAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _lead_detail_view_fields
    list_editable = comadm.standard_list_editable + _lead_detail_view_fields
    list_filter = comadm.standard_list_filter
    search_fields = comadm.standard_search_fields + ['viewer__first_name',
        'viewer__last_name']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _lead_detail_view_fields})]
    autocomplete_fields = ['lead', 'viewer']

_filter_form_post_fields = ['title', 'details', 'is_buying', 'is_selling',
'is_direct', 'is_agent', 'user_country', 'lead_country', 'is_initial_deposit',
'is_goods_shipped', 'is_payment_received', 'is_goods_received', 'is_others',
'user']
@admin.register(models.FilterFormPost)
class FilterFormPostAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _filter_form_post_fields
    list_editable = comadm.standard_list_editable + _filter_form_post_fields
    search_fields = comadm.standard_search_fields + _filter_form_post_fields

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _filter_form_post_fields})]
    autocomplete_fields = ['user']

_whatsapp_lead_author_click_fields = ['lead', 'contactor', 'count']
@admin.register(models.WhatsAppLeadAuthorClick)
class WhatsAppLeadAuthorClickAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + \
        _whatsapp_lead_author_click_fields
    list_editable = comadm.standard_list_editable + \
        _whatsapp_lead_author_click_fields
    search_fields = comadm.standard_search_fields + \
        _whatsapp_lead_author_click_fields

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _whatsapp_lead_author_click_fields})]
    autocomplete_fields = ['lead', 'contactor']

_whatsapp_click_fields = ['contactee', 'contactor', 'count']
@admin.register(models.WhatsAppClick)
class WhatsAppClickAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _whatsapp_click_fields
    list_editable = comadm.standard_list_editable + _whatsapp_click_fields
    search_fields = comadm.standard_search_fields + _whatsapp_click_fields

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _whatsapp_click_fields})]
    autocomplete_fields = ['contactee', 'contactor']

_whatsapp_message_body_fields = ['contactee', 'contactor', 'body']
@admin.register(models.WhatsAppMessageBody)
class WhatsAppMessageBodyAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _whatsapp_message_body_fields
    list_editable = comadm.standard_list_editable + \
        _whatsapp_message_body_fields
    search_fields = comadm.standard_search_fields + \
        _whatsapp_message_body_fields

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _whatsapp_message_body_fields})]
    autocomplete_fields = ['contactee', 'contactor']

_agent_query_fields = ['user', 'search', 'country']
@admin.register(models.AgentQuery)
class AgentQueryAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _agent_query_fields
    list_editable = comadm.standard_list_editable + _agent_query_fields
    search_fields = comadm.standard_search_fields + _agent_query_fields

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _agent_query_fields})]
    autocomplete_fields = ['user', 'country']

_lead_query_fields = ['user', 'search', 'wants_to', 'buy_country',
    'sell_country', 'sort_by']
@admin.register(models.LeadQuery)
class LeadQueryAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _lead_query_fields
    list_editable = comadm.standard_list_editable + _lead_query_fields
    search_fields = comadm.standard_search_fields + _lead_query_fields

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _lead_query_fields})]
    autocomplete_fields = ['user', 'buy_country', 'sell_country']