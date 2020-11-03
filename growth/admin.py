from django.contrib import admin
from . import models as mod
from common import admin as comadm

@admin.register(mod.GmassCampaignResult)
class GmassCampaignResultAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['email_address',
        'first_name', 'last_name', 'name_1', 'opens', 'clicks', 'replied',
        'unsubscribed', 'bounced', 'blocked', 'over_gmail_limit',
        'bounce_reason', 'gmail_response', 'email', 'gmass_campaign']
    list_editable = comadm.standard_list_editable + ['email_address',
        'first_name', 'last_name', 'name_1', 'opens', 'clicks', 'replied',
        'unsubscribed', 'bounced', 'blocked', 'over_gmail_limit',
        'bounce_reason', 'gmail_response', 'email', 'gmass_campaign']
    list_per_page = 1000
    list_filter = comadm.standard_list_filter + ['replied', 'unsubscribed',
        'bounced', 'blocked', 'over_gmail_limit']
    search_fields = ['id', 'email_address', 'first_name', 'last_name', 'name_1',
        'opens', 'clicks', 'replied', 'unsubscribed', 'bounced', 'blocked',
        'over_gmail_limit', 'bounce_reason', 'gmail_response', 'email',
        'gmass_campaign']
    ordering = comadm.standard_ordering
    show_full_result_count = True
    
    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': ['email_address', 'first_name',
            'last_name', 'name_1', 'opens', 'clicks', 'replied', 'unsubscribed',
            'bounced', 'blocked', 'over_gmail_limit', 'bounce_reason',
            'gmail_response']
        }),
        (None, {'fields': ['email', 'gmass_campaign']})
    ]
    autocomplete_fields = ['email', 'gmass_campaign']

@admin.register(mod.GmassCampaign)
class GmassCampaign(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['campaign_id', 'sent',
        'subject', 'spreadsheet']
    list_editable = comadm.standard_list_editable + ['campaign_id', 'sent',
        'subject', 'spreadsheet']
    list_per_page = 1000
    list_filter = comadm.standard_list_filter + ['sent']
    search_fields = ['id', 'campaign_id', 'sent', 'subject', 'spreadsheet']
    ordering = comadm.standard_ordering
    show_full_result_count = True
    
    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + \
        [(None, {'fields': ['campaign_id', 'sent', 'subject', 'spreadsheet']})]

@admin.register(mod.ChemicalClusterOfSingaporeResult)
class ChemicalClusterOfSingaporeAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['sourced', 'company_name',
        'telephone', 'fax', 'website', 'source_link']
    list_editable = comadm.standard_list_editable + ['sourced', 'company_name',
        'telephone', 'fax', 'website', 'source_link']
    list_per_page = 1000
    list_filter = comadm.standard_list_filter + ['sourced']
    search_fields = ['id', 'company_name', 'telephone', 'fax', 'website',
        'source_link']
    ordering = ['sourced'] + comadm.standard_ordering
    show_full_result_count = True
    
    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': ['sourced', 'source_link']}),
        (None, {'fields': ['company_name', 'telephone', 'fax', 'email_str',
            'website', 'address_str']}),
        (None, {'fields': ['company', 'email', 'phone_numbers', 'link',
            'address']})
    ]
    autocomplete_fields = ['company', 'email', 'phone_numbers', 'link',
        'address']

@admin.register(mod.Fibre2FashionResult)
class Fibre2FashionResultAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['sourced', 'source_link',
        'category', 'sub_category', 'email', 'email_domain', 'lead_type',
        'description']
    list_editable = comadm.standard_list_editable + ['sourced', 'source_link',
        'category', 'sub_category', 'email', 'email_domain', 'lead_type',
        'description']
    list_per_page = 1000
    list_filter = comadm.standard_list_filter + ['sourced']
    search_fields = ['id', 'source_link', 'category', 'sub_category', 'email',
        'email_domain', 'lead_type', 'description']
    ordering = ['sourced'] + comadm.standard_ordering
    show_full_result_count = True
    
    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': ['sourced', 'source_link']}),
        (None, {
            'fields': ['category', 'sub_category', 'email', 'email_domain',
                'lead_type', 'description']}),
        (None, {'fields': ['links', 'emails']})
    ]
    autocomplete_fields = ['links', 'emails']

@admin.register(mod.ZeroBounceResult)
class ZeroBounceResultAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['email_address', 'status',
        'sub_status', 'account', 'domain', 'first_name', 'last_name', 'gender',
        'free_email', 'mx_found', 'mx_record', 'smtp_provider', 'did_you_mean']
    list_editable = comadm.standard_list_editable + ['email_address', 'status',
        'sub_status', 'account', 'domain', 'first_name', 'last_name', 'gender',
        'free_email', 'mx_found', 'mx_record', 'smtp_provider', 'did_you_mean']
    list_per_page = 1000
    list_filter = comadm.standard_list_filter + ['status', 'sub_status', 'gender',
        'free_email', 'mx_found']
    search_fields = ['id', 'email_address', 'status', 'sub_status', 'account',
        'domain', 'first_name', 'last_name', 'gender', 'free_email', 'mx_found',
        'mx_record', 'smtp_provider', 'did_you_mean']
    ordering = ['email_address']
    show_full_result_count = True
    
    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        (None, {
            'fields': ['email_address', 'status',
            'sub_status', 'account', 'domain', 'first_name', 'last_name',
            'gender', 'free_email', 'mx_found', 'mx_record', 'smtp_provider',
            'did_you_mean']}),
        (None, {'fields': ['email']})
    ]
    autocomplete_fields = ['email']

@admin.register(mod.DataSource)
class DataSourceAdmin(comadm.ChoiceAdmin):
    pass

@admin.register(mod.SourcedEmail)
class SourcedEmailAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['sourced', 'source', 'email']
    list_editable = comadm.standard_list_editable + \
        ['sourced', 'source', 'email']
    list_per_page = 1000
    list_filter = comadm.standard_list_filter + ['sourced']
    search_fields = ['source', 'email']
    ordering = ['email']
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': ['sourced', 'source', 'email']})]
    autocomplete_fields = ['source', 'email']