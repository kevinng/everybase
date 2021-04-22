from django.contrib import admin

from . import models as mod
from common import admin as comadm

# --- Start: Inline ---

# class CompanyPhoneNumberInlineAdmin(admin.TabularInline):
#     model = mod.CompanyPhoneNumber
#     extra = 1
#     autocomplete_fields = ['rtype', 'company', 'phone_number']

# class CompanyAddressInlineAdmin(admin.TabularInline):
#     model = mod.CompanyAddress
#     extra = 1
#     autocomplete_fields = ['rtype', 'company', 'address']

# class CompanyLinkInlineAdmin(admin.TabularInline):
#     model = mod.CompanyLink
#     extra = 1
#     autocomplete_fields = ['rtype', 'link']

# class CompanyEmailInlineAdmin(admin.TabularInline):
#     model = mod.CompanyEmail
#     extra = 1
#     autocomplete_fields = ['rtype', 'company', 'email']

# class CompanyWeChatIDInlineAdmin(admin.TabularInline):
#     model = mod.CompanyWeChatID
#     extra = 1
#     autocomplete_fields = ['rtype', 'company', 'wechat_id']

# class PersonLinkInlineAdmin(admin.TabularInline):
#     model = mod.PersonLink
#     extra = 1
#     autocomplete_fields = ['rtype', 'link']

# class PersonCompanyInlineAdmin(admin.TabularInline):
#     model = mod.PersonCompany
#     extra = 1
#     autocomplete_fields = ['rtype', 'company']

# class PersonAddressInlineAdmin(admin.TabularInline):
#     model = mod.PersonAddress
#     extra = 1
#     autocomplete_fields = ['rtype', 'person', 'address']

# class PersonPhoneNumberInlineAdmin(admin.TabularInline):
#     model = mod.PersonPhoneNumber
#     extra = 1
#     autocomplete_fields = ['rtype', 'person', 'phone_number']

# class PersonEmailInlineAdmin(admin.TabularInline):
#     model = mod.PersonEmail
#     extra = 1
#     autocomplete_fields = ['rtype', 'person', 'email']

# class PersonWeChatIDInlineAdmin(admin.TabularInline):
#     model = mod.PersonWeChatID
#     extra = 1
#     autocomplete_fields = ['rtype', 'person', 'wechat_id']

# --- End: Inline ---

# @admin.register(
#     mod.PersonLinkType,
#     mod.PersonCompanyType,
#     mod.PersonAddressType,
#     mod.PersonPhoneNumberType,
#     mod.PersonEmailType,
#     mod.CompanyLinkType,
#     mod.CompanyAddressType,
#     mod.CompanyPhoneNumberType,
#     mod.CompanyEmailType,
#     mod.PhoneNumberType,
#     mod.BlackListReasonType,
#     mod.CompanyWeChatIDType,
#     mod.PersonWeChatIDType)
# class ChoiceAdmin(comadm.ChoiceAdmin):
#     pass

# _address_fields = ['address_1', 'address_2', 'address_3', 'address_1_cn',
#     'address_2_cn', 'address_3_cn', 'country', 'state', 'postal_code']
# @admin.register(mod.Address)
# class AddressAdmin(admin.ModelAdmin):
#     # List page settings
#     list_display = comadm.standard_list_display + _address_fields
#     list_editable = comadm.standard_list_editable + _address_fields
#     list_per_page = 50
#     list_filter = comadm.standard_list_filter + [
#         'company_address_relationships', 'person_address_relationships']
#     search_fields = ['id', 'address_1', 'address_2', 'address_3',
#         'address_1_cn', 'address_2_cn', 'address_3_cn',
#         'country__name', 'state__name', 'postal_code',
#         'company_address_relationships__company__company_name',
#         'person_address_relationships__person__given_name',
#         'person_address_relationships__person__family_name']
#     ordering = comadm.standard_ordering
#     show_full_result_count = True

#     # Details page settings
#     save_on_top = True
#     readonly_fields = comadm.standard_readonly_fields
#     fieldsets = comadm.standard_fieldsets + \
#         [(None, {'fields': _address_fields})]
#     autocomplete_fields = ['country', 'state']
#     inlines = [CompanyAddressInlineAdmin, PersonAddressInlineAdmin]

# _company_fields = ['company_name', 'company_name_wo_postfix', 'notes_md',
#     'domain']
# @admin.register(mod.Company)
# class CompanyAdmin(admin.ModelAdmin):
#     # List page settings
#     list_display = comadm.standard_list_display + _company_fields
#     list_editable = comadm.standard_list_editable + _company_fields
#     list_per_page = 50
#     list_filter = comadm.standard_list_filter
#     search_fields = ['id'] + _company_fields
#     ordering = comadm.standard_ordering
#     show_full_result_count = True

#     # Details page settings
#     save_on_top = True
#     readonly_fields = comadm.standard_readonly_fields
#     fieldsets = comadm.standard_fieldsets + \
#         [('Details', {'fields': _company_fields})]
#     inlines = [CompanyEmailInlineAdmin, CompanyPhoneNumberInlineAdmin,
#         CompanyAddressInlineAdmin, CompanyLinkInlineAdmin]

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

@admin.register(mod.Email)
class EmailAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['email', 'import_job']
    list_editable = comadm.standard_list_editable + ['email']
    list_per_page = 50
    list_filter = ['import_job'] + comadm.standard_list_filter
    search_fields = comadm.standard_search_fields + ['email']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': ['email', 'import_job']})
    ]
    autocomplete_fields = ['import_job']
    # inlines = [CompanyEmailInlineAdmin, PersonEmailInlineAdmin]

@admin.register(mod.InvalidEmail)
class InvalidEmailAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['email', 'import_job']
    list_editable = comadm.standard_list_editable + ['email']
    list_per_page = 50
    list_filter = ['import_job'] + comadm.standard_list_filter
    search_fields = comadm.standard_search_fields + ['email']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': ['email', 'import_job']})
    ]
    autocomplete_fields = ['import_job']

_user_fields = ['phone_number', 'name', 'is_banned', 'notes', 'email']
@admin.register(mod.User)
class UserAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['key'] + _user_fields
    list_editable = comadm.standard_list_editable + _user_fields
    list_per_page = 50
    list_filter = comadm.standard_list_filter
    search_fields = comadm.standard_search_fields + _user_fields
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = ['key'] + comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': ['key'] + _user_fields})
    ]
    autocomplete_fields = ['phone_number', 'email']

_accessed_url_fields = ['user', 'first_accessed', 'last_accessed', 'count',
    'url']
@admin.register(mod.AccessedURL)
class AccessedURLAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _accessed_url_fields
    list_editable = comadm.standard_list_editable + _accessed_url_fields
    list_per_page = 50
    list_filter = comadm.standard_list_filter
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
        'browser', 'browser_family', 'os', 'device', 'device_family']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _user_ip_device_fields + ['accessed_urls']})
    ]
    autocomplete_fields = ['user']

@admin.register(mod.ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_choice_list_display
    list_editable = comadm.standard_choice_list_editable
    list_per_page = 50
    list_filter = comadm.standard_choice_list_filter
    search_fields = comadm.standard_choice_search_fields
    ordering = comadm.standard_choice_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_choice_readonly_fields
    fieldsets = comadm.standard_choice_fieldsets

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
        ('Details', {'fields': ['display_name', 'notes']})
    ]
    autocomplete_fields = ['product_types']

_company_product_type_fields = ['popularity', 'company', 'product_type']
@admin.register(mod.CompanyProductType)
class CompanyProductTypeAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + \
        _company_product_type_fields
    list_editable = comadm.standard_list_editable + \
        _company_product_type_fields
    list_per_page = 50
    list_filter = comadm.standard_list_filter
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

_product_specification_type = ['display_name', 'notes', 'product_type']
@admin.register(mod.ProductSpecificationType)
class ProductSpecificationTypeAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _product_specification_type
    list_editable = comadm.standard_list_editable + _product_specification_type
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
        ('Details', {'fields': _product_specification_type})
    ]
    autocomplete_fields = ['product_type']

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
class IncotermAvailabilityAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_choice_list_display
    list_editable = comadm.standard_choice_list_editable
    list_per_page = 50
    list_filter = comadm.standard_choice_list_filter
    search_fields = comadm.standard_choice_search_fields
    ordering = comadm.standard_choice_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_choice_readonly_fields
    fieldsets = comadm.standard_choice_fieldsets

@admin.register(mod.Location)
class LocationAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_choice_list_display
    list_editable = comadm.standard_choice_list_editable
    list_per_page = 50
    list_filter = comadm.standard_choice_list_filter
    search_fields = comadm.standard_choice_search_fields
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_choice_readonly_fields
    fieldsets = comadm.standard_choice_fieldsets

_payment_term_fields = ['supply_quote', 'demand_quote']
@admin.register(mod.PaymentTerm)
class PaymentTermAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_choice_list_display + _payment_term_fields
    list_editable = comadm.standard_choice_list_editable + _payment_term_fields
    list_per_page = 50
    list_filter = comadm.standard_choice_list_filter
    search_fields = comadm.standard_choice_search_fields
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_choice_readonly_fields
    fieldsets = comadm.standard_choice_fieldsets + [
        ('Details', {'fields': _payment_term_fields})
    ]
    autocomplete_fields = _payment_term_fields

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


# _person_fields = ['given_name', 'family_name', 'notes_md']
# @admin.register(mod.Person)
# class PersonAdmin(admin.ModelAdmin):
#     # List page settings
#     list_display = comadm.standard_list_display + _person_fields
#     list_editable = comadm.standard_list_editable + _person_fields
#     list_per_page = 50
#     list_filter = comadm.standard_list_filter
#     search_fields = ['id'] + _person_fields
#     ordering = comadm.standard_ordering
#     show_full_result_count = True

#     # Details page settings
#     save_on_top = True
#     readonly_fields = comadm.standard_readonly_fields
#     fieldsets = comadm.standard_fieldsets + \
#         [('Details', {'fields': _person_fields})]
#     inlines = [PersonLinkInlineAdmin, PersonCompanyInlineAdmin,
#         PersonAddressInlineAdmin, PersonPhoneNumberInlineAdmin,
#         PersonEmailInlineAdmin]

# _link_fields = ['link']
# @admin.register(mod.Link)
# class LinkAdmin(admin.ModelAdmin):
#     # List page settings
#     list_display = comadm.standard_list_display + _link_fields
#     list_editable = comadm.standard_list_editable + _link_fields
#     list_per_page = 50
#     list_filter = comadm.standard_list_filter
#     search_fields = ['id', 'link']
#     ordering = comadm.standard_ordering
#     show_full_result_count = True

#     # Details page settings
#     save_on_top = True
#     readonly_fields = comadm.standard_readonly_fields
#     fieldsets = comadm.standard_fieldsets + \
#         [('Details', {'fields': _link_fields + ['languages']})]
#     autocomplete_fields = ['languages']

# _black_list_entry_fields = ['start', 'invalidated', 'reason', 'reason_md',
#     'email', 'phone_number', 'company', 'person']
# _black_list_entry_rel_fields = ['email', 'phone_number', 'company', 'person']
# @admin.register(mod.BlackListEntry)
# class BlackListEntryAdmin(admin.ModelAdmin):
#     # List page settings
#     list_display = comadm.standard_list_display + _black_list_entry_fields
#     list_editable = comadm.standard_list_editable + _black_list_entry_fields
#     list_per_page = 50
#     list_filter = comadm.standard_list_filter
#     search_fields = ['id', 'reason_md', 'email__email',
#         'phone_number__country_code', 'phone_number__national_number',
#         'company__company_name', 'person__given_name', 'person__family_name']
#     ordering = comadm.standard_ordering
#     show_full_result_count = True

#     # Details page settings
#     save_on_top = True
#     readonly_fields = comadm.standard_readonly_fields
#     fieldsets = comadm.standard_fieldsets + [
#             (None, {'fields': ['start', 'invalidated', 'reason', 'reason_md']}),
#             (None, {
#                 'fields': _black_list_entry_rel_fields,
#                 'description': 'At least one of these must be set'
#             })
#         ]
#     autocomplete_fields = _black_list_entry_rel_fields + ['reason']

# _wechat_id_fields = ['wechat_id']
# @admin.register(mod.WeChatID)
# class WeChatIDAdmin(admin.ModelAdmin):
#     # List page settings
#     list_display = comadm.standard_list_display + _wechat_id_fields
#     list_editable = comadm.standard_list_editable + _wechat_id_fields
#     list_per_page = 50
#     list_filter = comadm.standard_list_filter + _wechat_id_fields
#     search_fields = ['id'] + _wechat_id_fields
#     ordering = comadm.standard_ordering
#     show_full_result_count = True

#     # Details page settings
#     save_on_top = True
#     readonly_fields = comadm.standard_readonly_fields
#     fieldsets = comadm.standard_fieldsets + \
#         [('Details', {'fields': _wechat_id_fields})]
#     inlines = [CompanyWeChatIDInlineAdmin, PersonWeChatIDInlineAdmin]

# --- Start: Relationships ---

# _rel_list_display = comadm.standard_list_display + ['details_md', 'rtype']
# _prel_list_display = _rel_list_display + ['person']
# _crel_list_display = _rel_list_display + ['company']

# _rel_list_editable = comadm.standard_list_editable + ['details_md', 'rtype']
# _prel_list_editable = _rel_list_editable + ['person']
# _crel_list_editable = _rel_list_editable + ['company']

# _rel_list_search_fields = ['id', 'details_md', 'rtype__name']
# _prel_list_search_fields = _rel_list_search_fields + ['person__given_name',
#     'person__family_name']
# _crel_list_search_fields = _rel_list_search_fields + ['company__company_name']

# _rel_fieldsets_fields = ['details_md', 'rtype']
# _prel_fieldsets = lambda field: comadm.standard_fieldsets + [
#     (None, {'fields': _rel_fieldsets_fields + ['person', field]})]
# _crel_fieldsets = lambda field: comadm.standard_fieldsets + [
#     (None, {'fields': _rel_fieldsets_fields + ['company', field]})]

# _rel_autocomplete_fields = ['rtype']
# _prel_autocomplete_fields = _rel_autocomplete_fields + ['person']
# _crel_autocomplete_fields = _rel_autocomplete_fields + ['company']

# class RelationshipAdmin(admin.ModelAdmin):
#     # List page settings
#     list_per_page = 50
#     list_filter = comadm.standard_list_filter
#     ordering = comadm.standard_ordering
#     show_full_result_count = True

#     # Details page settings
#     save_on_top = True
#     readonly_fields = comadm.standard_readonly_fields

# @admin.register(mod.PersonLink)
# class PersonLinkAdmin(RelationshipAdmin):
#     # List page settings
#     list_display = _prel_list_display + ['link']
#     list_editable = _prel_list_editable + ['link']
#     search_fields = _prel_list_search_fields + ['link']

#     # Details page settings
#     fieldsets = _prel_fieldsets('link')
#     autocomplete_fields = _prel_autocomplete_fields + ['link']

# @admin.register(mod.PersonCompany)
# class PersonCompanyAdmin(RelationshipAdmin):
#     # List page settings
#     list_display = _prel_list_display + ['company']
#     list_editable = _prel_list_editable + ['company']
#     search_fields = _prel_list_search_fields + ['company']

#     # Details page settings
#     fieldsets = _prel_fieldsets('company')
#     autocomplete_fields = _prel_autocomplete_fields + ['company']

# @admin.register(mod.PersonAddress)
# class PersonAddressAdmin(RelationshipAdmin):
#     # List page settings
#     list_display = _prel_list_display + ['address']
#     list_editable = _prel_list_editable + ['address']
#     search_fields = _prel_list_search_fields + ['address']

#     # Details page settings
#     fieldsets = _prel_fieldsets('address')
#     autocomplete_fields = _prel_autocomplete_fields + ['address']

# @admin.register(mod.PersonPhoneNumber)
# class PersonPhoneNumberAdmin(RelationshipAdmin):
#     # List page settings
#     list_display = _prel_list_display + ['phone_number']
#     list_editable = _prel_list_editable + ['phone_number']
#     search_fields = _prel_list_search_fields + ['phone_number']

#     # Details page settings
#     fieldsets = _prel_fieldsets('phone_number')
#     autocomplete_fields = _prel_autocomplete_fields + ['phone_number']

# @admin.register(mod.PersonEmail)
# class PersonEmailAdmin(RelationshipAdmin):
#     # List page settings
#     list_display = _prel_list_display + ['email']
#     list_editable = _prel_list_editable + ['email']
#     search_fields = _prel_list_search_fields + ['email']

#     # Details page settings
#     fieldsets = _prel_fieldsets('email')
#     autocomplete_fields = _prel_autocomplete_fields + ['email']

# @admin.register(mod.PersonWeChatID)
# class PersonWeChatIDAdmin(RelationshipAdmin):
#     # List page settings
#     list_display = _prel_list_display + ['wechat_id']
#     list_editable = _prel_list_editable + ['wechat_id']
#     search_fields = _prel_list_search_fields + ['wechat_id__wechat_id']

#     # Details page settings
#     fieldsets = _prel_fieldsets('wechat_id')
#     autocomplete_fields = _prel_autocomplete_fields + ['wechat_id']

# @admin.register(mod.CompanyLink)
# class CompanyLinkAdmin(RelationshipAdmin):
#     # List page settings
#     list_display = _crel_list_display + ['link']
#     list_editable = _crel_list_editable + ['link']
#     search_fields = _crel_list_search_fields + ['link']

#     # Details page settings
#     fieldsets = _crel_fieldsets('link')
#     autocomplete_fields = _crel_autocomplete_fields + ['link']

# @admin.register(mod.CompanyAddress)
# class CompanyAddressAdmin(RelationshipAdmin):
#     # List page settings
#     list_display = _crel_list_display + ['address']
#     list_editable = _crel_list_editable + ['address']
#     search_fields = _crel_list_search_fields + ['address']

#     # Details page settings
#     fieldsets = _crel_fieldsets('address')
#     autocomplete_fields = _crel_autocomplete_fields + ['address']

# @admin.register(mod.CompanyPhoneNumber)
# class CompanyPhoneNumberAdmin(RelationshipAdmin):
#     # List page settings
#     list_display = _crel_list_display + ['phone_number']
#     list_editable = _crel_list_editable + ['phone_number']
#     search_fields = _crel_list_search_fields + ['phone_number']

#     # Details page settings
#     fieldsets = _crel_fieldsets('phone_number')
#     autocomplete_fields = _crel_autocomplete_fields + ['phone_number']

# @admin.register(mod.CompanyEmail)
# class CompanyEmailAdmin(RelationshipAdmin):
#     # List page settings
#     list_display = _crel_list_display + ['email']
#     list_editable = _crel_list_editable + ['email']
#     search_fields = _crel_list_search_fields + ['email']

#     # Details page settings
#     fieldsets = _crel_fieldsets('email')
#     autocomplete_fields = _crel_autocomplete_fields + ['email']

# @admin.register(mod.CompanyWeChatID)
# class CompanyWeChatIDAdmin(RelationshipAdmin):
#     # List page settings
#     list_display = _crel_list_display + ['wechat_id']
#     list_editable = _crel_list_editable + ['wechat_id']
#     search_fields = _crel_list_search_fields + ['wechat_id__wechat_id']

#     # Details page settings
#     fieldsets = _crel_fieldsets('wechat_id')
#     autocomplete_fields = _crel_autocomplete_fields + ['wechat_id']

# --- End: Relationships ---