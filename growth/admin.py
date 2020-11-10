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
    list_per_page = 50
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
    list_display = comadm.standard_list_display + ['sent', 'campaign_id',
        'subject', 'spreadsheet']
    list_editable = comadm.standard_list_editable + ['sent', 'campaign_id',
        'subject', 'spreadsheet']
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['sent']
    search_fields = ['id', 'sent', 'campaign_id', 'subject', 'spreadsheet']
    ordering = comadm.standard_ordering
    show_full_result_count = True
    
    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields + ['id']
    fieldsets = comadm.standard_fieldsets + \
        [(None, {'fields': ['sent', 'campaign_id', 'subject', 'spreadsheet']})]

@admin.register(mod.ChemicalClusterOfSingaporeResult)
class ChemicalClusterOfSingaporeAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['harvested', 'source_link',
        'company_name', 'telephone', 'fax', 'email_str', 'website',
        'address_str', 'company', 'email', 'phone_number', 'link', 'address']
    list_editable = comadm.standard_list_editable + ['harvested', 'source_link',
        'company_name', 'telephone', 'fax', 'email_str', 'website',
        'address_str', 'company', 'email', 'phone_number', 'link', 'address']
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['harvested']
    search_fields = ['id', 'source_link', 'company_name', 'telephone', 'fax',
        'email_str', 'website', 'address_str', 'company', 'email',
        'phone_number', 'link', 'address']
    ordering = comadm.standard_ordering + ['harvested']
    show_full_result_count = True
    
    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields + ['id']
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': ['harvested', 'source_link', 'company_name',
            'telephone', 'fax', 'email_str', 'website', 'address_str']}),
        (None, {'fields': ['company', 'email', 'phone_number', 'link',
            'address']})
    ]
    autocomplete_fields = ['company', 'email', 'phone_number', 'link',
        'address']

# @admin.register(mod.Fibre2FashionResult)
# class Fibre2FashionResultAdmin(admin.ModelAdmin):
#     # List page settings
#     list_display = comadm.standard_list_display + ['harvested', 'source_link',
#         'category', 'sub_category', 'email', 'email_domain', 'lead_type',
#         'description']
#     list_editable = comadm.standard_list_editable + ['harvested', 'source_link',
#         'category', 'sub_category', 'email', 'email_domain', 'lead_type',
#         'description']
#     list_per_page = 50
#     list_filter = comadm.standard_list_filter + ['harvested']
#     search_fields = ['id', 'source_link', 'category', 'sub_category', 'email',
#         'email_domain', 'lead_type', 'description']
#     ordering = ['harvested'] + comadm.standard_ordering
#     show_full_result_count = True
    
#     # Details page settings
#     save_on_top = True
#     readonly_fields = comadm.standard_readonly_fields
#     fieldsets = comadm.standard_fieldsets + [
#         (None, {'fields': ['harvested', 'source_link', 'category',
#             'sub_category', 'email', 'email_domain', 'lead_type',
#             'description']}),
#         (None, {'fields': ['links', 'emails']})]
#     autocomplete_fields = ['links', 'emails']

@admin.register(mod.ZeroBounceResult)
class ZeroBounceResultAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['import_job', 'generated',
        'email_str', 'status', 'sub_status', 'account', 'domain',
        'first_name', 'last_name', 'gender', 'free_email', 'mx_found',
        'mx_record', 'smtp_provider', 'did_you_mean', 'email', 'invalid_email',
        'did_you_mean_email']
    list_editable = comadm.standard_list_editable + ['import_job', 'generated',
        'email_str', 'status', 'sub_status', 'account', 'domain',
        'first_name', 'last_name', 'gender', 'free_email', 'mx_found',
        'mx_record', 'smtp_provider', 'did_you_mean', 'email', 'invalid_email',
        'did_you_mean_email']
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['generated', 'status',
        'sub_status', 'gender', 'free_email', 'mx_found']
    search_fields = ['id', 'import_job__description', 'email_str', 'status',
        'sub_status', 'account', 'domain', 'first_name', 'last_name', 'gender',
        'free_email', 'mx_found', 'mx_record', 'smtp_provider', 'did_you_mean',
        'email__email', 'invalid_email__email', 'did_you_mean_email__email']
    ordering = ['email_str']
    show_full_result_count = True
    
    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        (None, {
            'fields': ['import_job', 'generated', 'email_str', 'status',
            'sub_status', 'account', 'domain', 'first_name', 'last_name',
            'gender', 'free_email', 'mx_found', 'mx_record', 'smtp_provider',
            'did_you_mean']}),
        (None, {'fields': ['email', 'invalid_email', 'did_you_mean_email']})
    ]
    autocomplete_fields = ['import_job', 'email', 'invalid_email',
        'did_you_mean_email']

@admin.register(mod.DataSource)
class DataSourceAdmin(comadm.ChoiceAdmin):
    pass

@admin.register(mod.SourcedEmail)
class SourcedEmailAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['harvested', 'source',
        'email']
    list_editable = comadm.standard_list_editable + ['harvested', 'source',
        'email']
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['harvested', 'source']
    search_fields = ['id', 'source', 'email']
    ordering = ['harvested']
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields + ['id']
    fieldsets = comadm.standard_fieldsets + \
        [(None, {'fields': ['harvested', 'source', 'email']})]
    autocomplete_fields = ['source', 'email']

@admin.register(mod.ChemicalBookResult)
class ChemicalBookAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['harvested', 'source_url',
        'coy_name', 'coy_internal_href', 'coy_tel', 'coy_email', 'coy_href',
        'coy_nat']
    list_editable = comadm.standard_list_editable + ['harvested', 'source_url',
        'coy_name', 'coy_internal_href', 'coy_tel', 'coy_email', 'coy_href',
        'coy_nat']
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['harvested']
    search_fields = ['id', 'source_url', 'coy_name', 'coy_internal_href',
        'coy_tel', 'coy_email', 'coy_href', 'coy_nat']
    ordering = ['harvested']
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields + ['id']
    fieldsets = comadm.standard_fieldsets + \
        [(None, {'fields': ['harvested', 'source_url', 'coy_name',
            'coy_internal_href', 'coy_tel', 'coy_email', 'coy_href', 'coy_nat'
        ]})]

@admin.register(mod.LookChemResult)
class LookChemResultAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['id', 'harvested',
        'coy_name', 'contact_person', 'street_address', 'city',
        'province_state', 'country_region', 'zip_code', 'business_type', 'tel',
        'mobile', 'email', 'website', 'qq']
    list_editable = comadm.standard_list_editable + ['harvested', 'coy_name',
        'contact_person', 'street_address', 'city', 'province_state',
        'country_region', 'zip_code', 'business_type', 'tel', 'mobile', 'email',
        'website', 'qq']
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['harvested', 'city',
        'province_state', 'country_region', 'business_type']
    search_fields = ['id', 'coy_name', 'contact_person', 'street_address',
        'city', 'province_state', 'country_region', 'zip_code', 'business_type',
        'tel', 'mobile', 'email', 'website', 'qq']
    ordering = ['harvested']
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields + ['id']
    fieldsets = comadm.standard_fieldsets + \
        [(None, {'fields': ['harvested', 'coy_name',
            'contact_person', 'street_address', 'city', 'province_state',
            'country_region', 'zip_code', 'business_type', 'tel', 'mobile', 'email',
            'website', 'qq']})]

@admin.register(mod.WorldOfChemicalsResult)
class WorldOfChemicalsResultAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['id', 'harvested',
        'source_url', 'coy_id', 'coy_name', 'coy_about_html', 'coy_pri_contact',
        'coy_addr_1', 'coy_addr_2', 'coy_city', 'coy_state', 'coy_country',
        'coy_postal', 'coy_phone', 'coy_phone_2', 'coy_email',
        'coy_owner_email', 'coy_alt_email', 'coy_alt_email_2',
        'coy_alt_email_3', 'coy_website']
    list_editable = comadm.standard_list_editable + ['harvested', 'source_url',
        'coy_id', 'coy_name', 'coy_about_html', 'coy_pri_contact', 'coy_addr_1',
        'coy_addr_2', 'coy_city', 'coy_state', 'coy_country', 'coy_postal',
        'coy_phone', 'coy_phone_2', 'coy_email', 'coy_owner_email',
        'coy_alt_email', 'coy_alt_email_2', 'coy_alt_email_3', 'coy_website']
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['harvested', 'coy_city',
        'coy_state', 'coy_country']
    search_fields = ['id', 'source_url', 'coy_id', 'coy_name', 'coy_about_html',
        'coy_pri_contact', 'coy_addr_1', 'coy_addr_2', 'coy_city', 'coy_state',
        'coy_country', 'coy_postal', 'coy_phone', 'coy_phone_2', 'coy_email',
        'coy_owner_email', 'coy_alt_email', 'coy_alt_email_2',
        'coy_alt_email_3', 'coy_website']
    ordering = ['harvested']
    show_full_result_count = True
    
    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields + ['id']
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': ['harvested', 'source_url', 'coy_id', 'coy_name',
            'coy_about_html', 'coy_pri_contact', 'coy_addr_1', 'coy_addr_2',
            'coy_city', 'coy_state', 'coy_country', 'coy_postal', 'coy_phone',
            'coy_phone_2', 'coy_email', 'coy_owner_email', 'coy_alt_email',
            'coy_alt_email_2', 'coy_alt_email_3', 'coy_website']})]

@admin.register(mod.OKChemResult)
class OKChemResultAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['id', 'harvested', 'name',
        'country', 'request', 'email']
    list_editable = comadm.standard_list_editable + ['harvested', 'name',
        'country', 'request', 'email']
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['harvested', 'country']
    search_fields = ['id', 'source', 'name', 'country', 'request', 'email']
    ordering = ['harvested']
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields + ['id']
    fieldsets = comadm.standard_fieldsets + \
        [(None, {'fields': ['harvested', 'name', 'country', 'request',
            'email']})]