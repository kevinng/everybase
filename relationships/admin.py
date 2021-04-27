from django.contrib import admin

from . import models as mod
from common import admin as comadm

@admin.register(mod.PhoneNumberType)
class PhoneNumberTypeAdmin(comadm.ChoiceAdmin):
    pass

_phone_number_fields = ['country_code', 'national_number']
@admin.register(mod.PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _phone_number_fields
    list_editable = comadm.standard_list_editable + _phone_number_fields
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['country_code']
    search_fields = comadm.standard_search_fields + _phone_number_fields
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _phone_number_fields + ['types']})]
    autocomplete_fields = ['types']

_email_fields = ['email', 'import_job']
@admin.register(mod.Email)
class EmailAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _email_fields
    list_editable = comadm.standard_list_editable + ['email']
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['import_job']
    search_fields = comadm.standard_search_fields + ['email']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _email_fields})
    ]
    autocomplete_fields = ['import_job']

_invalid_email_fields = ['email', 'import_job']
@admin.register(mod.InvalidEmail)
class InvalidEmailAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _invalid_email_fields
    list_editable = comadm.standard_list_editable + ['email']
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['import_job']
    search_fields = comadm.standard_search_fields + ['email']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': _invalid_email_fields})
    ]
    autocomplete_fields = ['import_job']

_user_fields = ['phone_number', 'name', 'is_banned', 'notes', 'email']
@admin.register(mod.User)
class UserAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['key'] + _user_fields
    list_editable = comadm.standard_list_editable + _user_fields
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['is_banned']
    search_fields = comadm.standard_search_fields + _user_fields
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields + ['key']
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': ['key'] + _user_fields})
    ]
    autocomplete_fields = ['phone_number', 'email']

_accessed_url_fields = ['user', 'first_accessed', 'last_accessed', 'url',
    'count']
@admin.register(mod.AccessedURL)
class AccessedURLAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _accessed_url_fields
    list_editable = comadm.standard_list_editable + _accessed_url_fields
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['first_accessed',
        'last_accessed']
    search_fields = comadm.standard_search_fields + ['user__id', 'url']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': _accessed_url_fields})
    ]
    autocomplete_fields = ['user']

_user_ip_device_fields = ['user', 'first_accessed', 'last_accessed', 'count',
    'ip_address', 'is_mobile', 'is_tablet', 'is_touch_capable', 'is_pc',
    'is_bot', 'browser', 'browser_family', 'browser_version',
    'browser_version_string', 'os', 'os_version', 'os_version_string', 'device',
    'device_family']
@admin.register(mod.UserIPDevice)
class UserIPDeviceAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _user_ip_device_fields
    list_editable = comadm.standard_list_editable + _user_ip_device_fields
    list_per_page = 50
    list_filter = comadm.standard_list_filter
    search_fields = comadm.standard_search_fields + ['user__id', 'ip_address',
        'browser', 'browser_family', 'browser_version_string', 'os',
        'os_version_string', 'device', 'device_family']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _user_ip_device_fields + ['accessed_urls']})
    ]
    autocomplete_fields = ['user', 'accessed_urls']

@admin.register(mod.ProductType)
class ProductTypeAdmin(comadm.StandardChoiceAdmin):
    pass

_company_product_type_fields = ['popularity', 'company', 'product_type']
@admin.register(mod.CompanyProductType)
class CompanyProductTypeAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + \
        _company_product_type_fields
    list_editable = comadm.standard_list_editable + \
        _company_product_type_fields
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['product_type']
    search_fields = comadm.standard_search_fields + ['company__display_name',
        'company__notes', 'product_type__name', 'product_type__description']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _company_product_type_fields})
    ]
    autocomplete_fields = ['company', 'product_type']

_company_fields = ['display_name', 'notes']
@admin.register(mod.Company)
class CompanyAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _company_fields
    list_editable = comadm.standard_list_editable + _company_fields
    list_per_page = 50
    list_filter = comadm.standard_list_filter
    search_fields = comadm.standard_search_fields + _company_fields
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _company_fields})
    ]

_company_product_fields = ['popularity', 'company', 'product']
@admin.register(mod.CompanyProduct)
class CompanyProductAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _company_product_fields
    list_editable = comadm.standard_list_editable + _company_product_fields
    list_per_page = 50
    list_filter = comadm.standard_list_filter
    search_fields = comadm.standard_search_fields + ['company__display_name',
        'company__notes', 'product__display_name', 'product__notes']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _company_product_fields})
    ]
    autocomplete_fields = ['company', 'product']

_product_fields = ['display_name', 'notes', 'product_type']
@admin.register(mod.Product)
class ProductAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _product_fields
    list_editable = comadm.standard_list_editable + _product_fields
    list_per_page = 50
    list_filter = comadm.standard_list_filter
    search_fields = comadm.standard_search_fields + ['display_name', 'notes',
        'product_type__name', 'product_type__description']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _product_fields})
    ]
    autocomplete_fields = ['product_type']

_product_specification_type = ['display_name', 'notes', 'product_type']
@admin.register(mod.ProductSpecificationType)
class ProductSpecificationTypeAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _product_specification_type
    list_editable = comadm.standard_list_editable + _product_specification_type
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['product_type']
    search_fields = comadm.standard_search_fields + ['display_name', 'notes',
        'product_type__name', 'product_type__description']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _product_specification_type})
    ]
    autocomplete_fields = ['product_type']

_product_specification_fields = ['is_exists', 'value',
    'product_specification_type', 'product', 'supply', 'demand']
@admin.register(mod.ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + \
        _product_specification_fields
    list_editable = comadm.standard_list_editable + \
        _product_specification_fields
    list_per_page = 50
    list_filter = comadm.standard_list_filter + \
        ['is_exists', 'product_specification_type', 'product', 'supply',
            'demand']
    search_fields = comadm.standard_search_fields + [
        'product_specification_type__display_name',
        'product_specification_type__notes', 'product__display_name',
        'product__notes', 'supply__display_name', 'supply__notes',
        'demand__display_name', 'demand__notes']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
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

_lead_fields = ['product_type', 'company', 'product', 'user']
_lead_search_fields = ['product_type__name', 'product_type__description',
    'company__display_name', 'company__notes', 'product__display_name',
    'product__notes', 'user__name']

@admin.register(mod.Supply)
class SupplyAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _lead_fields
    list_editable = comadm.standard_list_editable + _lead_fields
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['product_type']
    search_fields = comadm.standard_search_fields + _lead_search_fields
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _lead_fields})
    ]
    autocomplete_fields = ['product_type', 'company', 'product', 'user']

@admin.register(mod.Demand)
class DemandAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _lead_fields
    list_editable = comadm.standard_list_editable + _lead_fields
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['product_type']
    search_fields = comadm.standard_search_fields + _lead_search_fields
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _lead_fields})
    ]
    autocomplete_fields = ['product_type', 'company', 'product', 'user']

_unit_of_measure_fields = ['plural_name', 'product_type']
@admin.register(mod.UnitOfMeasure)
class UnitOfMeasureAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_choice_list_display + _unit_of_measure_fields
    list_editable = comadm.standard_choice_list_editable + _unit_of_measure_fields
    list_per_page = 50
    list_filter = comadm.standard_choice_list_filter + ['product_type']
    search_fields = comadm.standard_choice_search_fields + \
        ['product_type__name', 'product_type__description']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_choice_readonly_fields
    fieldsets = comadm.standard_choice_fieldsets + [
        ('Details', {'fields': _unit_of_measure_fields})
    ]
    autocomplete_fields = ['product_type']

_lead_quote_fields = ['entered', 'price', 'price_uom', 'currency',
    'incoterm_availability', 'location', 'total_quantity', 'total_quantity_uom',
    'moq_quantity', 'moq_quantity_uom', 'delivery_interval_quantity',
    'delivery_interval_quantity_uom', 'delivery_interval_count',
    'delivery_interval_length', 'delivery_interval_uom',
    'commission_percentage_sales', 'commission_amount',
    'commission_amount_currency', 'commission_amount_uom']

@admin.register(mod.SupplyQuote)
class SupplyQuoteAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _lead_quote_fields
    list_editable = comadm.standard_list_editable + _lead_quote_fields
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['currency',
        'incoterm_availability', 'location', 'supply__product_type']
    search_fields = comadm.standard_search_fields + \
        ['supply__product_type__name']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _lead_quote_fields + ['supply']})
    ]
    autocomplete_fields = ['price_uom', 'currency', 'incoterm_availability',
        'location', 'total_quantity_uom', 'moq_quantity_uom',
        'delivery_interval_quantity_uom', 'commission_amount_currency',
        'commission_amount_uom', 'supply']

@admin.register(mod.DemandQuote)
class DemandQuoteAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _lead_quote_fields
    list_editable = comadm.standard_list_editable + _lead_quote_fields
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['currency',
        'incoterm_availability', 'location', 'demand__product_type']
    search_fields = comadm.standard_search_fields + \
        ['demand__product_type__name']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _lead_quote_fields + ['demand']})
    ]
    autocomplete_fields = ['price_uom', 'currency', 'incoterm_availability',
        'location', 'total_quantity_uom', 'moq_quantity_uom',
        'delivery_interval_quantity_uom', 'commission_amount_currency',
        'commission_amount_uom', 'demand']

_match_fields = ['buyer_sent', 'seller_sent', 'connected', 'supply_quote',
    'demand_quote']
@admin.register(mod.Match)
class MatchAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _match_fields
    list_editable = comadm.standard_list_editable + _match_fields
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['buyer_sent', 'seller_sent',
        'connected']
    search_fields = comadm.standard_search_fields + \
        ['supply_quote__supply__product_type__name',
        'demand_quote__demand__product_type__name']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _match_fields})
    ]
    autocomplete_fields = ['supply_quote', 'demand_quote']

_location_product_specification_type_fields = ['purpose', 'is_exists', 'value',
    'operator', 'location', 'product_specification_type']
@admin.register(mod.LocationProductSpecificationType)
class LocationProductSpecificationTypeAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + \
        _location_product_specification_type_fields
    list_editable = comadm.standard_list_editable + \
        _location_product_specification_type_fields
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['purpose', 'location',
        'product_specification_type']
    search_fields = comadm.standard_search_fields + \
        ['location__name', 'location__description',
        'product_specification_type__display_name',
        'product_specification_type__notes']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _location_product_specification_type_fields})
    ]
    autocomplete_fields = ['location', 'product_specification_type']