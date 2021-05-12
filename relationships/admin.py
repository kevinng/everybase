from django.contrib import admin

from . import models as mod
from common import admin as comadm

# ----- Start: Inlines -----

class CompanyProductTypeInlineAdmin(admin.TabularInline):
    model = mod.CompanyProductType
    extra = 1
    autocomplete_fields = ['product_type']

class CompanyProductInlineAdmin(admin.TabularInline):
    model = mod.CompanyProduct
    extra = 1
    autocomplete_fields = ['product']

class ProductTypeCompanyInlineAdmin(admin.TabularInline):
    model = mod.CompanyProductType
    extra = 1
    autocomplete_fields = ['company']

class ProductTypeProductInlineAdmin(admin.TabularInline):
    model = mod.Product
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
    inlines = [ProductTypeCompanyInlineAdmin, ProductTypeProductInlineAdmin]

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
    inlines = [CompanyProductTypeInlineAdmin, CompanyProductInlineAdmin]

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

_product_fields = ['url', 'product_type']
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
    inlines = [ProductCompanyInlineAdmin]

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
    'product_specification_type', 'product']
@admin.register(mod.ProductSpecification)
class ProductSpecificationAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + \
        _product_specification_fields
    list_editable = comadm.standard_list_editable + \
        _product_specification_fields
    list_filter = comadm.standard_list_filter + \
        ['is_exists', 'product_specification_type', 'product']
    search_fields = comadm.standard_search_fields + [
        'product_specification_type__display_name',
        'product_specification_type__notes', 'product__display_name',
        'product__notes', 'supply__display_name', 'supply__notes',
        'demand__display_name', 'demand__notes']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _product_specification_fields})
    ]
    autocomplete_fields = ['product_specification_type', 'product']

@admin.register(mod.IncotermAvailability)
class IncotermAvailabilityAdmin(comadm.StandardChoiceAdmin):
    pass

@admin.register(mod.Location)
class LocationAdmin(comadm.StandardChoiceAdmin):
    pass