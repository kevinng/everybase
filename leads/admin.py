from django.contrib import admin
from common import admin as comadm
from leads import models
from sorl.thumbnail.admin import AdminImageMixin

_lead_image_fields = ['lead', 'image']
@admin.register(models.LeadImage)
class LeadImageAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = _lead_image_fields
    list_display_links = ['lead']
    list_editable = ['image']
    search_fields = ['lead__id']

    fieldsets = [(None, {'fields': _lead_image_fields})]
    autocomplete_fields = ['lead']

class InlineLeadImageAdmin(AdminImageMixin, admin.TabularInline):
    model = models.LeadImage

_lead_fields = ['author', 'buy_country', 'sell_country', 'lead_type', 'details',
    'commission', 'avg_deal_size', 'other_agent_details', 'internal_notes',
    'onboarding', 'onboarded', 'title', 'author_type', 'country',
    'commission_payable_by', 'commission_payable_after']
@admin.register(models.Lead)
class LeadAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['uuid'] + _lead_fields
    list_editable = comadm.standard_list_editable + _lead_fields
    list_filter = comadm.standard_list_filter + ['buy_country', 'sell_country',
        'lead_type', 'onboarding', 'onboarded']
    search_fields = comadm.standard_search_fields + ['details',
        'internal_notes', 'other_comm_details']

    # Details page settings
    readonly_fields = comadm.standard_readonly_fields + ['uuid']
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _lead_fields})]
    autocomplete_fields = ['author', 'buy_country', 'sell_country']
    inlines = [InlineLeadImageAdmin]

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