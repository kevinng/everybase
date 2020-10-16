from django.contrib import admin
from .models import (GmassCampaignResult, GmassCampaign,
    ChemicalClusterOfSingaporeResult, Fibre2FashionResult, ZeroBounceResult,
    DataSource, SourcedEmail)
from common.admin import (standard_list_display, standard_list_filter,
    standard_ordering, standard_readonly_fields, standard_fieldsets,
    standard_list_editable)

admin.site.register(DataSource)
admin.site.register(SourcedEmail)

@admin.register(GmassCampaignResult)
class GmassCampaignResultAdmin(admin.ModelAdmin):
    # List page settings
    list_display = standard_list_display + ['first_name',
        'last_name', 'name_1', 'opens', 'clicks', 'replied', 'unsubscribed',
        'bounced', 'blocked', 'over_gmail_limit', 'bounce_reason',
        'gmail_response', 'email', 'gmass_campaign']
    list_editable = standard_list_editable + ['first_name', 'last_name',
        'name_1', 'opens', 'clicks', 'replied', 'unsubscribed', 'bounced',
        'blocked', 'over_gmail_limit', 'bounce_reason', 'gmail_response',
        'email', 'gmass_campaign']
    list_per_page = 1000
    list_filter = standard_list_filter + ['replied', 'unsubscribed', 'bounced',
        'blocked', 'over_gmail_limit']
    search_fields = ['id', 'first_name', 'last_name', 'name_1',
        'opens', 'clicks', 'replied', 'unsubscribed', 'bounced', 'blocked',
        'over_gmail_limit', 'bounce_reason', 'gmail_response', 'email',
        'gmass_campaign']
    ordering = standard_ordering
    show_full_result_count = True
    
    # Details page settings
    save_on_top = True
    readonly_fields = standard_readonly_fields
    fieldsets = standard_fieldsets + [
        ('Result details', {'fields': ['email_address', 'first_name',
            'last_name', 'name_1', 'opens', 'clicks', 'replied', 'unsubscribed',
            'bounced', 'blocked', 'over_gmail_limit', 'bounce_reason',
            'gmail_response']
        }),
        ('Model references', {'fields': ['email', 'gmass_campaign']})
    ]
    autocomplete_fields = ['email', 'gmass_campaign']

@admin.register(GmassCampaign)
class GmassCampaign(admin.ModelAdmin):
    # List page settings
    list_display = standard_list_display + ['campaign_id', 'sent', 'subject',
        'spreadsheet']
    list_editable = standard_list_editable + ['campaign_id', 'sent', 'subject',
        'spreadsheet']
    list_per_page = 1000
    list_filter = standard_list_filter + ['sent']
    search_fields = ['id', 'campaign_id', 'sent', 'subject', 'spreadsheet']
    ordering = standard_ordering
    show_full_result_count = True
    
    # Details page settings
    save_on_top = True
    readonly_fields = standard_readonly_fields
    fieldsets = standard_fieldsets + [
        ('Result details', {'fields': ['campaign_id', 'sent', 'subject',
            'spreadsheet']
        })
    ]

@admin.register(ChemicalClusterOfSingaporeResult)
class ChemicalClusterOfSingaporeAdmin(admin.ModelAdmin):
    # List page settings
    list_display = standard_list_display + ['sourced', 'company_name',
        'telephone', 'fax', 'website', 'source_link']
    list_editable = standard_list_editable + ['sourced', 'company_name',
        'telephone', 'fax', 'website', 'source_link']
    list_per_page = 1000
    list_filter = standard_list_filter + ['sourced']
    search_fields = ['id', 'company_name', 'telephone', 'fax', 'website',
        'source_link']
    ordering = ['sourced'] + standard_ordering
    show_full_result_count = True
    
    # Details page settings
    save_on_top = True
    readonly_fields = standard_readonly_fields
    fieldsets = standard_fieldsets + [
        ('Source', {'fields': ['sourced', 'source_link']}),
        ('Result details', {
            'fields': ['company_name', 'telephone', 'fax', 'email_str', 'website',
                'address_str']
        }),
        ('Model references', {
            'fields': ['company', 'email', 'phone_numbers', 'link', 'address']
        })
    ]
    autocomplete_fields = ['company', 'email', 'phone_numbers', 'link',
        'address']

@admin.register(Fibre2FashionResult)
class Fibre2FashionResultAdmin(admin.ModelAdmin):
    # List page settings
    list_display = standard_list_display + ['sourced', 'source_link',
        'category', 'sub_category', 'email', 'email_domain', 'lead_type',
        'description']
    list_editable = standard_list_editable + ['sourced', 'source_link',
        'category', 'sub_category', 'email', 'email_domain', 'lead_type',
        'description']
    list_per_page = 1000
    list_filter = standard_list_filter + ['sourced']
    search_fields = ['id', 'source_link', 'category', 'sub_category', 'email',
        'email_domain', 'lead_type', 'description']
    ordering = ['sourced'] + standard_ordering
    show_full_result_count = True
    
    # Details page settings
    save_on_top = True
    readonly_fields = standard_readonly_fields
    fieldsets = standard_fieldsets + [
        ('Source', {'fields': ['sourced', 'source_link']}),
        ('Result details', {
            'fields': ['category', 'sub_category', 'email', 'email_domain',
                'lead_type', 'description']
        }),
        ('Model references', {
            'fields': ['links', 'emails']
        })
    ]
    autocomplete_fields = ['links', 'emails']

@admin.register(ZeroBounceResult)
class ZeroBounceResultAdmin(admin.ModelAdmin):
    # List page settings
    list_display = standard_list_display + ['email_address', 'status',
        'sub_status', 'account', 'domain', 'first_name', 'last_name', 'gender',
        'free_email', 'mx_found', 'mx_record', 'smtp_provider', 'did_you_mean']
    list_editable = standard_list_editable + ['email_address', 'status',
        'sub_status', 'account', 'domain', 'first_name', 'last_name', 'gender',
        'free_email', 'mx_found', 'mx_record', 'smtp_provider', 'did_you_mean']
    list_per_page = 1000
    list_filter = standard_list_filter + ['status', 'sub_status', 'gender',
        'free_email', 'mx_found']
    search_fields = ['id', 'email_address', 'status', 'sub_status', 'account',
        'domain', 'first_name', 'last_name', 'gender', 'free_email', 'mx_found',
        'mx_record', 'smtp_provider', 'did_you_mean']
    ordering = ['email_address']
    show_full_result_count = True
    
    # Details page settings
    save_on_top = True
    readonly_fields = standard_readonly_fields
    fieldsets = standard_fieldsets + [
        ('Result details', {
            'fields': ['email_address', 'status',
            'sub_status', 'account', 'domain', 'first_name', 'last_name',
            'gender', 'free_email', 'mx_found', 'mx_record', 'smtp_provider',
            'did_you_mean']
        }),
        ('Model references', {
            'fields': ['email']
        })
    ]
    autocomplete_fields = ['email']