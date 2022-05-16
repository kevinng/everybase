from lzma import MODE_FAST
from django.contrib import admin
from common import admin as comadm
from files import admin as fiadm
from leads import models

_application_query_log_fields = ['user', 'status']
@admin.register(models.ApplicationQueryLog)
class ApplicationQueryLogAdmin(comadm.StandardAdmin):
    # List page settings
    list_per_page = 100
    list_display = comadm.standard_list_display + _application_query_log_fields
    list_editable = comadm.standard_list_editable + _application_query_log_fields
    list_filter = comadm.standard_list_filter + ['status']
    search_fields = comadm.standard_search_fields + ['user__first_name',
        'user__last_name', 'user__id']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _application_query_log_fields})]

class ApplicationFollowUpInlineAdmin(admin.TabularInline):
    model = models.ApplicationFollowUp
    extra = 1
    fields = ['id', 'created', 'application', 'notes']
    readonly_fields = ['id', 'created']
    autocomplete_fields = ['application']

@admin.register(models.Application)
class ApplicationAdmin(comadm.StandardAdmin):
    # List page settings
    list_per_page = 100
    list_display = ['id', 'lead', 'applicant', 'last_messaged', 'last_followed_up', 'stopped_follow_up', 'created', 'has_experience', 'has_buyers']
    list_editable = [] # Override to speed up loading
    list_filter = ['last_messaged', 'lead__lead_type', 'created', 'stopped_follow_up', 'has_experience', 'has_buyers']
    search_fields = ['id', 'lead__headline', 'applicant__first_name', 'applicant__last_name']

    # Details page settings
    fieldsets = [
        (None, {'fields': ['id']}),
        ('Application details', {'fields': ['lead', 'applicant', 'has_experience', 'has_buyers', 'questions', 'answers', 'applicant_comments']}),
        ('Timestamps', {'fields': ['last_messaged', 'stopped_follow_up', 'created', 'updated' , 'deleted']})
    ]
    autocomplete_fields = ['lead', 'applicant']
    inlines = [ApplicationFollowUpInlineAdmin]

@admin.register(models.ApplicationFollowUp)
class ApplicationFollowUpAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = ['id', 'created', 'application', 'notes']
    list_editable = [] # Override to speed up loading
    search_fields = ['id', 'application__id', 'notes']

    # Details page settings
    fieldsets = [
        (None, {'fields': ['id']}),
        ('Details', {'fields': ['application', 'notes']}),
        ('Timestamps', {'fields': ['created', 'updated', 'deleted']})
    ]
    autocomplete_fields = ['application']

@admin.register(models.ApplicationMessage)
class ApplicationMessageAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = ['id', 'created', 'application', 'author', 'body']
    list_editable = [] # Override to speed up loading
    search_fields = ['id', 'application__id', 'author__first_name', 'author__last_name', 'body']

    # Details page settings
    fieldsets = [
        (None, {'fields': ['id']}),
        ('Details', {'fields': ['application', 'author', 'body']}),
        ('Timestamps', {'fields': ['created', 'updated', 'deleted']})
    ]
    autocomplete_fields = ['application', 'author']

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

@admin.register(models.Lead)
class LeadAdmin(comadm.StandardAdmin):
    # List page settings
    list_per_page = 100
    list_display = ['id', 'created', 'author', 'lead_type', 'headline', 'details', 'min_commission_percentage', 'max_commission_percentage', 'buy_country', 'sell_country', 'author_type']
    list_editable = [] # Override to speed up loading
    list_filter = ['created', 'lead_type', 'author_type']
    search_fields = ['id', 'headline', 'details', 'author__first_name', 'author__last_name', 'internal_notes']

    # Details page settings
    readonly_fields = comadm.standard_readonly_fields + ['uuid', 'slug_link', 'slug_tokens']
    fieldsets = [
        (None, {'fields': ['id', 'uuid']}),
        ('Details', {'fields': ['author', 'lead_type', 'headline', 'details', 'min_commission_percentage', 'max_commission_percentage', 'buy_country', 'sell_country', 'author_type', 'questions']}),
        ('Meta', {'fields': ['internal_notes', 'slug_link', 'slug_tokens', 'impressions', 'clicks']}),
        ('Timestamps', {'fields': ['created', 'updated', 'deleted']}),
        ('Not in use', {'fields': ['title', 'currency', 'comm_details', 'need_agent', 'country', 'agent_job', 'avg_deal_size', 'commission_payable_by', 'commission_payable_after',
            'commission_payable_after_other', 'commission_earnings', 'commission_quantity_unit_string', 'commission_type_other', 'other_comm_details', 'is_comm_negotiable', 'is_promoted',
            'question_1', 'question_2', 'question_3', 'need_logistics_agent', 'other_logistics_agent_details']})
    ]
    inlines = [fiadm.FileInlineAdmin]
    autocomplete_fields = ['author', 'currency', 'buy_country', 'sell_country', 'country']

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

@admin.register(models.LeadQuery)
class LeadQueryAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = ['id', 'created', 'user', 'search_phrase', 'country', 'min_commission_percentage', 'max_commission_percentage']
    list_editable = [] # Override to speed up listing
    search_fields = ['id', 'search_phrase', 'user__first_name', 'user__last_name']

    # Details page settings
    fieldsets = [
        (None, {'fields': ['id']}),
        ('Details', {'fields': ['user', 'search_phrase', 'country', 'min_commission_percentage', 'max_commission_percentage']}),
        ('Timestamps', {'fields': ['created', 'updated', 'deleted']}),
        ('Not in use', {'fields': ['buy_country', 'sell_country', 'count']})
    ]
    autocomplete_fields = ['user']