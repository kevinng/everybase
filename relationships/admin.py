from django.contrib import admin

from . import models as mod
from processor import models as promod
from common import admin as comadm

# ----- Start: Inlines -----

class CompanyMatchingKeywordInlineAdmin(admin.TabularInline):
    model = promod.MatchingKeyword
    extra = 1
    exclude = ['currency', 'excluded_price', 'location',
        'incoterm_availability', 'application', 'product_type', 'product',
        'product_specification_type', 'unit_of_measure']

class CompanyProductTypeInlineAdmin(admin.TabularInline):
    model = mod.CompanyProductType
    extra = 1
    autocomplete_fields = ['product_type']

class CompanyProductInlineAdmin(admin.TabularInline):
    model = mod.CompanyProduct
    extra = 1
    autocomplete_fields = ['product']

class ProductTypeMatchingKeywordInlineAdmin(admin.TabularInline):
    model = promod.MatchingKeyword
    extra = 1
    exclude = ['currency', 'excluded_price', 'location',
        'incoterm_availability', 'application', 'company', 'product',
        'product_specification_type', 'unit_of_measure']

class ProductTypeCompanyInlineAdmin(admin.TabularInline):
    model = mod.CompanyProductType
    extra = 1
    autocomplete_fields = ['company']

class ProductTypeProductInlineAdmin(admin.TabularInline):
    model = mod.Product
    extra = 1

class ProductMatchingKeywordInlineAdmin(admin.TabularInline):
    model = promod.MatchingKeyword
    exclude = ['currency', 'excluded_price', 'location',
        'incoterm_availability', 'application', 'company', 'product_type',
        'product_specification_type', 'unit_of_measure']
    extra = 1

class ProductCompanyInlineAdmin(admin.TabularInline):
    model = mod.CompanyProduct
    extra = 1
    autocomplete_fields = ['company']

# ----- End: Inlines -----

@admin.register(mod.PhoneNumberType)
class PhoneNumberTypeAdmin(comadm.ChoiceAdmin):
    pass

_phone_number_fields = ['country_code', 'national_number']
@admin.register(mod.PhoneNumber)
class PhoneNumberAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _phone_number_fields
    list_editable = comadm.standard_list_editable + _phone_number_fields
    list_filter = comadm.standard_list_filter + ['country_code']
    search_fields = comadm.standard_search_fields + _phone_number_fields

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _phone_number_fields + ['types']})]
    autocomplete_fields = ['types']

_email_fields = ['email', 'import_job']
@admin.register(mod.Email)
class EmailAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _email_fields
    list_editable = comadm.standard_list_editable + ['email']
    list_filter = comadm.standard_list_filter + ['import_job']
    search_fields = comadm.standard_search_fields + ['email']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _email_fields})
    ]
    autocomplete_fields = ['import_job']

_invalid_email_fields = ['email', 'import_job']
@admin.register(mod.InvalidEmail)
class InvalidEmailAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _invalid_email_fields
    list_editable = comadm.standard_list_editable + ['email']
    list_filter = comadm.standard_list_filter + ['import_job']
    search_fields = comadm.standard_search_fields + ['email']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': _invalid_email_fields})
    ]
    autocomplete_fields = ['import_job']

_user_fields = ['phone_number', 'name', 'is_banned', 'notes', 'email']
@admin.register(mod.User)
class UserAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['key'] + _user_fields
    list_editable = comadm.standard_list_editable + _user_fields
    list_filter = comadm.standard_list_filter + ['is_banned']
    search_fields = comadm.standard_search_fields + _user_fields

    # Details page settings
    readonly_fields = comadm.standard_readonly_fields + ['key']
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': ['key'] + _user_fields})
    ]
    autocomplete_fields = ['phone_number', 'email']

_accessed_url_fields = ['user', 'first_accessed', 'last_accessed', 'url',
    'count']
@admin.register(mod.AccessedURL)
class AccessedURLAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _accessed_url_fields
    list_editable = comadm.standard_list_editable + _accessed_url_fields
    list_filter = comadm.standard_list_filter + ['first_accessed',
        'last_accessed']
    search_fields = comadm.standard_search_fields + ['user__id', 'url']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _accessed_url_fields})
    ]
    autocomplete_fields = ['user']

_user_ip_device_fields = ['user', 'first_accessed', 'last_accessed', 'count',
    'ip_address', 'is_mobile', 'is_tablet', 'is_touch_capable', 'is_pc',
    'is_bot', 'browser', 'browser_family', 'browser_version',
    'browser_version_string', 'os', 'os_version', 'os_version_string', 'device',
    'device_family']
@admin.register(mod.UserIPDevice)
class UserIPDeviceAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _user_ip_device_fields
    list_editable = comadm.standard_list_editable + _user_ip_device_fields
    search_fields = comadm.standard_search_fields + ['user__id', 'ip_address',
        'browser', 'browser_family', 'browser_version_string', 'os',
        'os_version_string', 'device', 'device_family']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _user_ip_device_fields + ['accessed_urls']})
    ]
    autocomplete_fields = ['user', 'accessed_urls']

@admin.register(mod.ProductType)
class ProductTypeAdmin(comadm.StandardChoiceAdmin):
    inlines = [ProductTypeMatchingKeywordInlineAdmin,
        ProductTypeCompanyInlineAdmin, ProductTypeProductInlineAdmin]

_company_product_type_fields = ['popularity', 'company', 'product_type']
@admin.register(mod.CompanyProductType)
class CompanyProductTypeAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + \
        _company_product_type_fields
    list_editable = comadm.standard_list_editable + \
        _company_product_type_fields
    list_filter = comadm.standard_list_filter + ['product_type']
    search_fields = comadm.standard_search_fields + ['company__display_name',
        'company__notes', 'product_type__name', 'product_type__description']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _company_product_type_fields})
    ]
    autocomplete_fields = ['company', 'product_type']

_company_fields = ['url']
@admin.register(mod.Company)
class CompanyAdmin(comadm.StandardChoiceAdmin):
    # List page settings
    list_display = comadm.standard_choice_list_display + _company_fields
    list_editable = comadm.standard_choice_list_editable + _company_fields
    search_fields = comadm.standard_choice_search_fields + _company_fields

    # Details page settings
    fieldsets = comadm.standard_choice_fieldsets + [
        ('Details', {'fields': _company_fields})
    ]
    inlines = [CompanyMatchingKeywordInlineAdmin, CompanyProductTypeInlineAdmin,
        CompanyProductInlineAdmin]

_company_product_fields = ['popularity', 'company', 'product']
@admin.register(mod.CompanyProduct)
class CompanyProductAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _company_product_fields
    list_editable = comadm.standard_list_editable + _company_product_fields
    search_fields = comadm.standard_search_fields + ['company__display_name',
        'company__notes', 'product__display_name', 'product__notes']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _company_product_fields})
    ]
    autocomplete_fields = ['company', 'product']

_product_fields = ['product_type']
@admin.register(mod.Product)
class ProductAdmin(comadm.StandardChoiceAdmin):
    # List page settings
    list_display = comadm.standard_choice_list_display + _product_fields
    list_editable = comadm.standard_choice_list_editable + _product_fields
    search_fields = comadm.standard_choice_search_fields + [
        'product_type__name', 'product_type__description']

    # Details page settings
    fieldsets = comadm.standard_choice_fieldsets + [
        ('Details', {'fields': _product_fields})
    ]
    autocomplete_fields = ['product_type']
    inlines = [ProductMatchingKeywordInlineAdmin, ProductCompanyInlineAdmin]

_product_specification_type = ['product_type']
@admin.register(mod.ProductSpecificationType)
class ProductSpecificationTypeAdmin(comadm.StandardChoiceAdmin):
    # List page settings
    list_display = comadm.standard_choice_list_display + \
        _product_specification_type
    list_editable = comadm.standard_choice_list_editable + \
        _product_specification_type
    list_filter = comadm.standard_choice_list_filter + ['product_type']
    search_fields = comadm.standard_choice_search_fields + \
        ['display_name', 'notes', 'product_type__name',
            'product_type__description']

    # Details page settings
    fieldsets = comadm.standard_choice_fieldsets + [
        ('Details', {'fields': _product_specification_type})
    ]
    autocomplete_fields = ['product_type']

_product_specification_fields = ['is_exists', 'string_value', 'float_value',
    'product_specification_type', 'product', 'supply', 'demand']
@admin.register(mod.ProductSpecification)
class ProductSpecificationAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + \
        _product_specification_fields
    list_editable = comadm.standard_list_editable + \
        _product_specification_fields
    list_filter = comadm.standard_list_filter + \
        ['is_exists', 'product_specification_type', 'product', 'supply',
            'demand']
    search_fields = comadm.standard_search_fields + [
        'product_specification_type__display_name',
        'product_specification_type__notes', 'product__display_name',
        'product__notes', 'supply__display_name', 'supply__notes',
        'demand__display_name', 'demand__notes']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _product_specification_fields})
    ]
    autocomplete_fields = ['product_specification_type', 'product', 'supply',
        'demand']

@admin.register(mod.IncotermAvailability)
class IncotermAvailabilityAdmin(comadm.StandardChoiceAdmin):
    pass

@admin.register(mod.Location)
class LocationAdmin(comadm.StandardChoiceAdmin):
    pass

_payment_term_fields = ['supply_quote', 'demand_quote']
@admin.register(mod.PaymentTerm)
class PaymentTermAdmin(comadm.StandardChoiceAdmin):
    # List page settings
    list_display = comadm.standard_choice_list_display + _payment_term_fields
    list_editable = comadm.standard_choice_list_editable + _payment_term_fields

    # Details page settings
    fieldsets = comadm.standard_choice_fieldsets + [
        ('Quotes', {'fields': _payment_term_fields})
    ]
    autocomplete_fields = _payment_term_fields

_packing_fields = ['base_quantity', 'base_uom', 'pack_uom', 'supply_quote',
    'demand_quote']
@admin.register(mod.Packing)
class PackingAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _packing_fields
    list_editable = comadm.standard_list_editable + _packing_fields
    list_filter = comadm.standard_list_filter + ['base_uom', 'pack_uom']
    search_fields = comadm.standard_search_fields + [
        'base_uom__name', 'base_uom__description', 'pack_uom__name',
        'pack_uom__description', 'supply_quote__product_type__name',
        'supply_quote__product_type__description',
        'demand_quote__product_type__name',
        'demand_quote__product_type__description']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _packing_fields})
    ]
    autocomplete_fields = ['base_uom', 'pack_uom', 'supply_quote',
        'demand_quote']

_unit_of_measure_fields = ['plural_name', 'product_type']
@admin.register(mod.UnitOfMeasure)
class UnitOfMeasureAdmin(comadm.StandardChoiceAdmin):
    # List page settings
    list_display = comadm.standard_choice_list_display + _unit_of_measure_fields
    list_editable = comadm.standard_choice_list_editable + \
        _unit_of_measure_fields
    list_filter = comadm.standard_choice_list_filter + ['product_type']
    search_fields = comadm.standard_choice_search_fields + \
        ['product_type__name', 'product_type__description']

    # Details page settings
    fieldsets = comadm.standard_choice_fieldsets + [
        ('Details', {'fields': _unit_of_measure_fields})
    ]
    autocomplete_fields = ['product_type']

_excluded_price_fields = ['supply_quote', 'demand_quote']
@admin.register(mod.ExcludedPrice)
class ExcludedPriceAdmin(comadm.StandardChoiceAdmin):
    # list page settings
    list_display = comadm.standard_choice_list_display + _excluded_price_fields
    list_editable = comadm.standard_choice_list_editable + \
        _excluded_price_fields    
    list_filter = comadm.standard_choice_list_filter + _excluded_price_fields
    search_fields = comadm.standard_choice_search_fields + \
        ['supply_quote__supply__product_type__name',
        'supply_quote__supply__product_type__description',
        'demand_quote__demand__product_type__name',
        'demand_quote__demand__product_type__description']

    # Details page settings
    fieldsets = comadm.standard_choice_fieldsets + [
        ('Details', {'fields': _excluded_price_fields})
    ]
    autocomplete_fields = _excluded_price_fields

_lead_fields = ['product_type', 'company', 'product', 'user']
_lead_search_fields = ['product_type__name', 'product_type__description',
    'company__display_name', 'company__notes', 'product__display_name',
    'product__notes', 'user__name']
_lead_autocomplete_fields = ['product_type', 'company', 'product', 'user']

@admin.register(mod.Supply)
class SupplyAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _lead_fields
    list_editable = comadm.standard_list_editable + _lead_fields
    list_filter = comadm.standard_list_filter + ['product_type']
    search_fields = comadm.standard_search_fields + _lead_search_fields

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _lead_fields})
    ]
    autocomplete_fields = _lead_autocomplete_fields

@admin.register(mod.Demand)
class DemandAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _lead_fields
    list_editable = comadm.standard_list_editable + _lead_fields
    list_filter = comadm.standard_list_filter + ['product_type']
    search_fields = comadm.standard_search_fields + _lead_search_fields

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _lead_fields})
    ]
    autocomplete_fields = _lead_autocomplete_fields

_lead_quote_fields = ['entered', 'price', 'price_uom', 'currency',
    'incoterm_availability', 'location', 'total_quantity', 'total_quantity_uom',
    'moq_quantity', 'moq_quantity_uom', 'delivery_interval_quantity',
    'delivery_interval_quantity_uom', 'delivery_interval_count',
    'delivery_interval_length', 'delivery_interval_uom',
    'commission_percentage_sales', 'commission_amount',
    'commission_amount_currency', 'commission_amount_uom']
_lead_autocomplete_fields = ['price_uom', 'currency', 'incoterm_availability',
    'location', 'total_quantity_uom', 'moq_quantity_uom',
    'delivery_interval_quantity_uom', 'commission_amount_currency',
    'commission_amount_uom']

@admin.register(mod.SupplyQuote)
class SupplyQuoteAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _lead_quote_fields
    list_editable = comadm.standard_list_editable + _lead_quote_fields
    list_filter = comadm.standard_list_filter + ['currency',
        'incoterm_availability', 'location', 'supply__product_type']
    search_fields = comadm.standard_search_fields + \
        ['supply__product_type__name']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _lead_quote_fields + ['supply']})
    ]
    autocomplete_fields = _lead_autocomplete_fields + ['supply']

@admin.register(mod.DemandQuote)
class DemandQuoteAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _lead_quote_fields
    list_editable = comadm.standard_list_editable + _lead_quote_fields
    list_filter = comadm.standard_list_filter + ['currency',
        'incoterm_availability', 'location', 'demand__product_type']
    search_fields = comadm.standard_search_fields + \
        ['demand__product_type__name']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _lead_quote_fields + ['demand']})
    ]
    autocomplete_fields = _lead_autocomplete_fields + ['demand']

_match_fields = ['buyer_sent', 'seller_sent', 'connected', 'supply_quote',
    'demand_quote']
@admin.register(mod.Match)
class MatchAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _match_fields
    list_editable = comadm.standard_list_editable + _match_fields
    list_filter = comadm.standard_list_filter + ['buyer_sent', 'seller_sent',
        'connected']
    search_fields = comadm.standard_search_fields + \
        ['supply_quote__supply__product_type__name',
        'demand_quote__demand__product_type__name']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _match_fields})
    ]
    autocomplete_fields = ['supply_quote', 'demand_quote']

_location_product_specification_type_fields = ['purpose', 'is_exists', 'value',
    'operator', 'location', 'product_specification_type']
@admin.register(mod.LocationProductSpecificationType)
class LocationProductSpecificationTypeAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + \
        _location_product_specification_type_fields
    list_editable = comadm.standard_list_editable + \
        _location_product_specification_type_fields
    list_filter = comadm.standard_list_filter + ['purpose', 'location',
        'product_specification_type']
    search_fields = comadm.standard_search_fields + \
        ['location__name', 'location__description',
        'product_specification_type__display_name',
        'product_specification_type__notes']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _location_product_specification_type_fields})
    ]
    autocomplete_fields = ['location', 'product_specification_type']

_top_level_domain_fields = ['domain_type', 'sponsoring_organization']
@admin.register(mod.TopLevelDomain)
class TopLevelDomainAdmin(comadm.ChoiceAdmin):
    # List page settings
    list_display = comadm.choice_list_display + _top_level_domain_fields
    list_editable = comadm.choice_list_editable + _top_level_domain_fields
    search_fields = comadm.choice_search_fields + _top_level_domain_fields

    # Details page settings
    fieldsets = comadm.choice_fieldsets + [
        ('Details', {'fields': _top_level_domain_fields})
    ]

@admin.register(mod.Application)
class ApplicationAdmin(comadm.ChoiceAdmin):
    pass