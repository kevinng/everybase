from django.contrib import admin
from .models import (PersonLinkType, PersonLink, PersonCompanyType,
    PersonAddressType, PersonAddress, PersonPhoneNumberType, PersonPhoneNumber,
    PersonEmailType, PersonEmail, CompanyLinkType, CompanyLink,
    CompanyAddressType, CompanyAddress, CompanyPhoneNumberType,
    CompanyPhoneNumber, CompanyEmailType, CompanyEmail, Person, Company, Email,
    LinkType, Link, AddressType, Address, PhoneNumberType, PhoneNumber)
from common.admin import (ChoiceAdmin, standard_list_display,
    standard_list_editable, standard_list_filter, standard_ordering,
    standard_readonly_fields, standard_fieldsets)

@admin.register(PersonLinkType, PersonCompanyType, PersonAddressType,
    PersonPhoneNumberType, PersonEmailType, CompanyLinkType, CompanyAddressType,
    CompanyPhoneNumberType, CompanyEmailType, LinkType, AddressType,
    PhoneNumberType)
class ChoiceAdmin(ChoiceAdmin):
    pass

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    # List page settings
    list_display = standard_list_display + ['address_1', 'address_2',
        'address_3', 'country', 'state', 'postal_code']
    list_editable = standard_list_editable + ['address_1', 'address_2',
        'address_3', 'country', 'state', 'postal_code']
    list_per_page = 1000
    list_filter = standard_list_filter + ['country', 'state']
    search_fields = ['id', 'address_1', 'address_2', 'address_3', 'country',
        'state', 'postal_code']
    ordering = standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = standard_readonly_fields
    fieldsets = standard_fieldsets + [
        ('Address', {'fields': ['address_1', 'address_2', 'address_3',
            'country', 'state', 'postal_code']})
    ]
    autocomplete_fields = ['country', 'state']

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    # List page settings
    list_display = standard_list_display + ['company_name',
        'company_name_wo_postfix', 'notes_md']
    list_editable = standard_list_editable + ['company_name',
        'company_name_wo_postfix', 'notes_md']
    list_per_page = 1000
    list_filter = standard_list_filter
    search_fields = ['id', 'company_name', 'company_name_wo_postfix',
        'notes_md']
    ordering = standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = standard_readonly_fields
    fieldsets = standard_fieldsets + [
        ('Details', {'fields': ['company_name', 'company_name_wo_postfix',
            'notes_md']})
    ]

@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    # List page settings
    list_display = standard_list_display + ['country_code', 'national_number']
    list_editable = standard_list_editable + ['country_code', 'national_number']
    list_per_page = 1000
    list_filter = standard_list_filter + ['country_code']
    search_fields = ['id', 'country_code', 'national_number']
    ordering = standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = standard_readonly_fields
    fieldsets = standard_fieldsets + [
        ('Phone number', {'fields': ['country_code', 'national_number']})
    ]

@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    # List page settings
    list_display = standard_list_display + ['email']
    list_editable = standard_list_editable + ['email']
    list_per_page = 1000
    list_filter = standard_list_filter
    search_fields = ['id', 'email']
    ordering = standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = standard_readonly_fields
    fieldsets = standard_fieldsets + [
        ('Details', {'fields': ['email']})
    ]

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    # List page settings
    list_display = standard_list_display + ['given_name', 'family_name',
        'country', 'state', 'notes_md']
    list_editable = standard_list_editable + ['given_name', 'family_name',
        'country', 'state', 'notes_md']
    list_per_page = 1000
    list_filter = standard_list_filter
    search_fields = ['id', 'given_name', 'family_name', 'country', 'state',
        'notes_md']
    ordering = standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = standard_readonly_fields
    fieldsets = standard_fieldsets + [
        ('Details', {'fields': ['given_name', 'family_name', 'country', 'state',
            'notes_md']})
    ]
    autocomplete_fields = ['country', 'state']

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    # List page settings
    list_display = standard_list_display + ['last_visited_okay', 'link']
    list_editable = standard_list_editable + ['last_visited_okay', 'link']
    list_per_page = 1000
    list_filter = standard_list_filter
    search_fields = ['id', 'link']
    ordering = standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = standard_readonly_fields
    fieldsets = standard_fieldsets + [
        ('Details', {'fields': ['last_visited_okay', 'link']})
    ]

admin.site.register(PersonLink)
admin.site.register(PersonAddress)
admin.site.register(PersonPhoneNumber)
admin.site.register(PersonEmail)
admin.site.register(CompanyLink)
admin.site.register(CompanyAddress)
admin.site.register(CompanyPhoneNumber)
admin.site.register(CompanyEmail)