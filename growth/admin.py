from django.contrib import admin
from . import models as mod
from common import admin as comadm

@admin.register(mod.GmassEmailStatus)
class GmassEmailStatusAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['bounced', 'bounce_reason',
        'unsubscribed', 'email', 'invalid_email']
    list_per_page = 50
    list_filter = ['bounced', 'unsubscribed'] + comadm.standard_list_filter
    search_fields = ['id', 'bounce_reason', 'email__email',
        'invalid_email__email']
    ordering = comadm.standard_ordering
    show_full_result_count = True
    
    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': ['bounced', 'bounce_reason', 'unsubscribed', 'email',
            'invalid_email']})
    ]
    autocomplete_fields = ['email', 'invalid_email']

@admin.register(mod.GmassCampaignResult)
class GmassCampaignResultAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['import_job',
        'email_address', 'first_name', 'last_name', 'name_1', 'opens', 'clicks',
        'replied', 'unsubscribed', 'bounced', 'blocked', 'over_gmail_limit',
        'gmail_response', 'email', 'invalid_email', 'gmass_campaign']
    list_per_page = 50
    list_filter = ['import_job', 'opens', 'clicks', 'replied', 'unsubscribed',
        'bounced', 'blocked', 'over_gmail_limit'] + comadm.standard_list_filter
    search_fields = ['id', 'email_address', 'first_name', 'last_name', 'name_1',
        'replied', 'unsubscribed', 'bounced', 'blocked', 'over_gmail_limit',
        'gmail_response']
    ordering = comadm.standard_ordering
    show_full_result_count = True
    
    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': ['email_address', 'first_name',
            'last_name', 'name_1', 'opens', 'clicks', 'replied', 'unsubscribed',
            'bounced', 'blocked', 'over_gmail_limit', 'invalid_email',
            'gmail_response', 'email', 'gmass_campaign']
        })
    ]
    autocomplete_fields = ['email', 'gmass_campaign']

@admin.register(mod.GmassCampaign)
class GmassCampaign(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['sent', 'campaign_id',
        'subject', 'spreadsheet', 'report_url', 'report_last_accessed']
    list_per_page = 50
    list_filter = ['sent'] + comadm.standard_list_filter
    search_fields = ['id', 'campaign_id', 'subject', 'spreadsheet',
        'report_url']
    ordering = ['sent'] + comadm.standard_ordering
    show_full_result_count = True
    
    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields + ['id']
    fieldsets = comadm.standard_fieldsets + \
        [(None, {'fields': ['sent', 'campaign_id', 'subject', 'spreadsheet',
            'report_url', 'report_last_accessed']})]

@admin.register(mod.ChemicalClusterOfSingaporeCompany)
class ChemicalClusterOfSingaporeCompanyAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['email_str',
        'executive_email_str', 'email', 'invalid_email', 'executive_email',
        'invalid_executive_email', 'import_job', 'harvested', 'source_url',
        'company_name', 'telephone', 'fax', 'website', 'address',
        'nature_of_business', 'executive_name', 'executive_telephone']
    list_per_page = 50
    list_filter = ['harvested', 'import_job'] + comadm.standard_list_filter
    search_fields = ['id', 'source_url', 'company_name',
        'telephone', 'fax', 'email_str', 'website', 'address',
        'nature_of_business', 'executive_name', 'executive_telephone',
        'executive_email_str']
    ordering = ['harvested'] + comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields + ['id']
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': ['import_job', 'harvested', 'source_url',
            'company_name', 'telephone', 'fax', 'email_str', 'website',
            'address', 'nature_of_business', 'executive_name',
            'executive_telephone', 'executive_email_str', 'email',
            'invalid_email', 'executive_email', 'invalid_executive_email']})
    ]
    autocomplete_fields = ['import_job', 'email', 'invalid_email',
        'executive_email', 'invalid_executive_email']

@admin.register(mod.ChemicalClusterOfSingaporeProduct)
class ChemicalClusterOfSingaporeProductAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['import_job', 'harvested',
        'source_url', 'company_name', 'product']
    list_per_page = 50
    list_filter = ['harvested'] + comadm.standard_list_filter
    search_fields = ['id', 'source_url', 'company_name', 'product']
    ordering = ['harvested'] + comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields + ['id']
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': ['import_job', 'harvested', 'source_url',
            'company_name', 'product']})
    ]
    autocomplete_fields = ['import_job']

@admin.register(mod.ChemicalClusterOfSingaporeService)
class ChemicalClusterOfSingaporeServiceAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['import_job', 'harvested',
        'source_url', 'company_name', 'service']
    list_per_page = 50
    list_filter = ['harvested'] + comadm.standard_list_filter
    search_fields = ['id', 'source_url', 'company_name', 'service']
    ordering = ['harvested'] + comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields + ['id']
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': ['import_job', 'harvested', 'source_url',
            'company_name', 'service']})
    ]
    autocomplete_fields = ['import_job']

@admin.register(mod.Fibre2FashionBuyingOffer)
class Fibre2FashionBuyingOfferAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['email',
        'invalid_email', 'import_job', 'harvested', 'source_url', 'category',
        'sub_category', 'title', 'reference_no', 'description', 'email_str',
        'product_info_html']
    list_per_page = 50
    list_filter = ['import_job', 'harvested', 'category', 'sub_category'] + \
        comadm.standard_list_filter
    search_fields = ['id', 'source_url', 'category', 'sub_category', 'title',
        'reference_no', 'description', 'email_str', 'product_info_html']
    ordering = ['harvested'] + comadm.standard_ordering
    show_full_result_count = True
    
    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': ['import_job', 'harvested', 'source_link', 'category',
            'sub_category', 'reference_no', 'description', 'email_str',
            'product_info_html', 'email', 'invalid_email']})]
    autocomplete_fields = ['import_job', 'email', 'invalid_email']

@admin.register(mod.Fibre2FashionSellingOffer)
class Fibre2FashionSellingOfferAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['email', 'invalid_email',
        'import_job', 'harvested', 'source_url', 'category', 'sub_category',
        'title', 'reference_no', 'description', 'email_str', 'company_name',
        'company_address', 'product_info_html']
    list_per_page = 50
    list_filter = ['import_job', 'harvested', 'category', 'sub_category'] + \
        comadm.standard_list_filter
    search_fields = ['id', 'source_url', 'category', 'sub_category', 'title',
        'reference_no', 'description', 'email_str', 'company_name',
        'company_address', 'product_info_html']
    ordering = ['harvested'] + comadm.standard_ordering
    show_full_result_count = True
    
    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': ['import_job', 'harvested', 'source_link', 'category',
            'sub_category', 'reference_no', 'description', 'email_str',
            'company_name', 'company_address', 'product_info_html', 'email',
            'invalid_email']})]
    autocomplete_fields = ['import_job', 'email', 'invalid_email']

@admin.register(mod.ZeroBounceResult)
class ZeroBounceResultAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['email', 'invalid_email',
        'did_you_mean_email', 'import_job', 'generated', 'email_str', 'status',
        'sub_status', 'account', 'domain', 'first_name', 'last_name', 'gender',
        'free_email', 'mx_found', 'mx_record', 'smtp_provider', 'did_you_mean']
    list_per_page = 50
    list_filter = ['import_job', 'generated', 'status', 'sub_status', 'gender',
        'free_email', 'mx_found'] + comadm.standard_list_filter
    search_fields = ['id', 'email_str', 'status', 'sub_status', 'account',
        'domain', 'first_name', 'last_name', 'gender', 'free_email',
        'mx_found', 'mx_record', 'smtp_provider', 'did_you_mean']
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
            'did_you_mean', 'email', 'invalid_email', 'did_you_mean_email']})
    ]
    autocomplete_fields = ['import_job', 'email', 'invalid_email',
        'did_you_mean_email']

@admin.register(mod.ChemicalBookSupplier)
class ChemicalBookSupplierAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['email', 'invalid_email',
        'import_job', 'harvested', 'source_url', 'company_name', 'internal_url',
        'telephone', 'email_str', 'corporate_site_url', 'nationality']
    list_per_page = 50
    list_filter = ['import_job', 'harvested'] + comadm.standard_list_filter
    search_fields = ['id', 'source_url', 'company_name', 'internal_url',
        'telephone', 'email_str', 'corporate_site_url', 'nationality']
    ordering = ['harvested']
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields + ['id']
    fieldsets = comadm.standard_fieldsets + \
        [(None, {'fields': ['import_job', 'harvested',
            'source_url', 'company_name', 'internal_url', 'telephone',
            'email_str', 'corporate_site_url', 'nationality', 'email',
            'invalid_email']})]
    autocomplete_fields = ['import_job', 'email', 'invalid_email']

@admin.register(mod.LookChemSupplier)
class LookChemSupplierAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['email', 'invalid_email',
        'harvested', 'company_name', 'contact_person', 'street_address', 'city',
        'province_state', 'country_region', 'zip_code', 'business_type', 'tel',
        'mobile', 'email_str', 'website', 'qq']
    list_per_page = 50
    list_filter = ['harvested', 'business_type'] + comadm.standard_list_filter
    search_fields = ['id', 'company_name', 'contact_person', 'street_address',
        'city', 'province_state', 'country_region', 'zip_code', 'business_type',
        'tel', 'mobile', 'email', 'website', 'qq']
    ordering = ['harvested']
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields + ['id']
    fieldsets = comadm.standard_fieldsets + \
        [(None, {'fields': ['harvested', 'company_name',
            'contact_person', 'street_address', 'city', 'province_state',
            'country_region', 'zip_code', 'business_type', 'tel', 'mobile',
            'email_str', 'website', 'qq', 'email', 'invalid_email']})]
    autocomplete_fields = ['email', 'invalid_email']

@admin.register(mod.WorldOfChemicalsSupplier)
class WorldOfChemicalsSupplierAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['email', 'owner_email',
        'alt_email', 'alt_email_2', 'alt_email_3', 'invalid_email',
        'invalid_owner_email', 'invalid_alt_email', 'invalid_alt_email_2',
        'invalid_alt_email_3', 'import_job', 'harvested', 'source_url',
        'coy_id', 'coy_name', 'coy_about_html', 'coy_pri_contact', 'coy_addr_1',
        'coy_addr_2', 'coy_city', 'coy_state', 'coy_country', 'coy_postal',
        'coy_phone', 'coy_phone_2', 'coy_email', 'coy_owner_email',
        'coy_alt_email', 'coy_alt_email_2', 'coy_alt_email_3', 'coy_website']
    list_per_page = 50
    list_filter = ['harvested'] + comadm.standard_list_filter
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
            'coy_alt_email_2', 'coy_alt_email_3', 'coy_website', 'email',
            'owner_email', 'alt_email', 'alt_email_2', 'alt_email_3',
            'invalid_email', 'invalid_owner_email', 'invalid_alt_email',
            'invalid_alt_email_2', 'invalid_alt_email_3']})]
    autocomplete_fields = ['email', 'owner_email', 'alt_email', 'alt_email_2',
        'alt_email_3', 'invalid_email', 'invalid_owner_email',
        'invalid_alt_email', 'invalid_alt_email_2', 'invalid_alt_email_3']

@admin.register(mod.OKChemBuyingRequest)
class OKChemBuyingRequestAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['request', 'email', 'domain',
        'import_job', 'harvested', 'name', 'country']
    list_per_page = 50
    list_filter = ['import_job', 'harvested'] + comadm.standard_list_filter
    search_fields = ['id', 'source', 'name', 'country', 'request', 'email']
    ordering = ['harvested']
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields + ['id']
    fieldsets = comadm.standard_fieldsets + \
        [(None, {'fields': ['harvested', 'name', 'country', 'request',
            'email', 'domain']})]

_note_fields = ['user', 'note_type', 'text', 'deadline',
    'done']
@admin.register(mod.Note)
class NoteAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _note_fields
    list_editable = comadm.standard_list_editable + ['text', 'deadline', 'done']
    list_filter = comadm.standard_list_filter + ['deadline', 'done']
    search_fields = comadm.standard_search_fields + ['text']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [(None, {'fields': _note_fields})]
    autocomplete_fields = ['user']