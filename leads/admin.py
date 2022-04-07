from django.contrib import admin
from common import admin as comadm
from files import admin as fiadm
from leads import models

_lead_comment_fields = ['lead', 'commentor', 'body']
@admin.register(models.LeadComment)
class LeadCommentAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _lead_comment_fields
    list_editable = comadm.standard_list_editable + _lead_comment_fields
    search_fields = comadm.standard_search_fields + ['lead__first_name',
        'lead__last_name', 'commentor__first_name', 'commentor__last_name',
        'body']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': _lead_comment_fields})
    ]
    autocomplete_fields = ['lead', 'commentor']

_lead_fields = [
    'author', 'is_promoted',

    'lead_type', 'author_type', 'buy_country', 'sell_country', 'details',
    'agent_job',

    'commission_type', 'commission_percentage', 'commission_earnings',
    'commission_quantity_unit_string', 'commission_type_other', 'other_agent_details',

    'is_comm_negotiable',

    'impressions', 'clicks',

    'internal_notes', 'slug_link', 'slug_tokens',

    # Not in use

    'title',

    'need_agent', 'country',

    'avg_deal_size', 'commission_payable_by',

    'commission_payable_after', 'commission_payable_after_other',

    'need_logistics_agent', 'other_logistics_agent_details'
]
@admin.register(models.Lead)
class LeadAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['uuid'] + _lead_fields
    list_editable = comadm.standard_list_editable + _lead_fields
    list_filter = comadm.standard_list_filter + ['buy_country', 'sell_country',
        'lead_type', 'need_agent', 'commission_payable_by', 'commission_type',
        'is_comm_negotiable', 'commission_payable_after', 'need_logistics_agent']
    search_fields = comadm.standard_search_fields + ['details',
        'other_agent_details', 'other_logistics_agent_details', 'slug_link',
        'slug_tokens', 'internal_notes']

    # Details page settings
    readonly_fields = comadm.standard_readonly_fields + ['uuid']
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _lead_fields})]
    autocomplete_fields = ['author', 'buy_country', 'sell_country']
    inlines = [fiadm.FileInlineAdmin]

_saved_lead_fields = ['active', 'saver', 'lead']
@admin.register(models.SavedLead)
class SavedLeadAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _saved_lead_fields
    list_editable = comadm.standard_list_editable + _saved_lead_fields
    list_filter = comadm.standard_list_filter + ['active']
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

_lead_query_fields = [
    'user',
    'commented_only',
    'saved_only',
    'buy_sell',
    'direct_middleman',
    'buy_country',
    'sell_country',
    'goods_services',
    'need_agent',
    'commission_type',
    'commission_type_other',
    'min_commission',
    'max_commission',
    'min_avg_deal',
    'max_avg_deal',
    'comm_negotiable',
    'commission_payable_after',
    'commission_payable_after_other',
    'other_agent_details',
    'need_logistics_agent',
    'logistics_agent_details'
]
@admin.register(models.LeadQuery)
class LeadQueryAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _lead_query_fields
    list_editable = comadm.standard_list_editable + _lead_query_fields
    search_fields = comadm.standard_search_fields + _lead_query_fields

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _lead_query_fields})]
    autocomplete_fields = ['user']