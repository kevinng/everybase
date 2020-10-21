from django.contrib import admin
from .models import (PersonLinkType, PersonLink, PersonCompany,
    PersonCompanyType, PersonAddressType, PersonAddress, PersonPhoneNumberType,
    PersonPhoneNumber, PersonEmailType, PersonEmail, CompanyLinkType,
    CompanyLink, CompanyAddressType, CompanyAddress, CompanyPhoneNumberType,
    CompanyPhoneNumber, CompanyEmailType, CompanyEmail, Person, Company, Email,
    Link, Address, PhoneNumberType, PhoneNumber)
from common.admin import (ChoiceAdmin, standard_list_display,
    standard_list_editable, standard_list_filter, standard_ordering,
    standard_readonly_fields, standard_fieldsets)

@admin.register(PersonLinkType, PersonCompanyType, PersonAddressType,
    PersonPhoneNumberType, PersonEmailType, CompanyLinkType, CompanyAddressType,
    CompanyPhoneNumberType, CompanyEmailType, PhoneNumberType)
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

relationship_list_display = standard_list_display + ['details_md']
relationship_list_editable = standard_list_editable + ['details_md']
relationship_list_search_fields = ['id', 'details_md']
relationship_fieldsets = standard_fieldsets + [
    ('Details', {'fields': ['details_md']})
]

class RelationshipAdmin(admin.ModelAdmin):
    # List page settings
    list_per_page = 1000
    list_filter = standard_list_filter
    ordering = standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = standard_readonly_fields
    fieldsets = relationship_fieldsets

@admin.register(PersonLink)
class PersonLinkAdmin(RelationshipAdmin):
    # List page settings
    list_display = relationship_list_display + ['rtype', 'person', 'link']
    list_editable = relationship_list_editable + ['rtype', 'person', 'link']
    search_fields = relationship_list_search_fields + ['rtype', 'person',
        'link']

    # Details page settings
    fieldsets = relationship_fieldsets + [
        ('Model references', {'fields': ['rtype', 'person', 'link']})
    ]
    autocomplete_fields = ['rtype', 'person', 'link']

@admin.register(PersonCompany)
class PersonLinkAdmin(RelationshipAdmin):
    # List page settings
    list_display = relationship_list_display + ['rtype', 'person', 'company']
    list_editable = relationship_list_editable + ['rtype', 'person', 'company']
    search_fields = relationship_list_search_fields + ['rtype', 'person',
        'company']

    # Details page settings
    fieldsets = relationship_fieldsets + [
        ('Model references', {'fields': ['rtype', 'person', 'company']})
    ]
    autocomplete_fields = ['rtype', 'person', 'company']

@admin.register(PersonAddress)
class PersonAddressAdmin(RelationshipAdmin):
    # List page settings
    list_display = relationship_list_display + ['rtype', 'person', 'address']
    list_editable = relationship_list_editable + ['rtype', 'person', 'address']
    search_fields = relationship_list_search_fields + ['rtype', 'person',
        'address']

    # Details page settings
    fieldsets = relationship_fieldsets + [
        ('Model references', {'fields': ['rtype', 'person', 'address']})
    ]
    autocomplete_fields = ['rtype', 'person', 'address']

@admin.register(PersonPhoneNumber)
class PersonPhoneNumberAdmin(RelationshipAdmin):
    # List page settings
    list_display = relationship_list_display + ['rtype', 'person',
        'phone_number']
    list_editable = relationship_list_editable + ['rtype', 'person',
        'phone_number']
    search_fields = relationship_list_search_fields + ['rtype', 'person',
        'phone_number']

    # Details page settings
    fieldsets = relationship_fieldsets + [
        ('Model references', {'fields': ['rtype', 'person', 'phone_number']})
    ]
    autocomplete_fields = ['rtype', 'person', 'phone_number']

@admin.register(PersonEmail)
class PersonEmailAdmin(RelationshipAdmin):
    # List page settings
    list_display = relationship_list_display + ['rtype', 'person',
        'email']
    list_editable = relationship_list_editable + ['rtype', 'person',
        'email']
    search_fields = relationship_list_search_fields + ['rtype', 'person',
        'email']

    # Details page settings
    fieldsets = relationship_fieldsets + [
        ('Model references', {'fields': ['rtype', 'person', 'email']})
    ]
    autocomplete_fields = ['rtype', 'person', 'email']

@admin.register(CompanyLink)
class CompanyLinkAdmin(RelationshipAdmin):
    # List page settings
    list_display = relationship_list_display + ['rtype', 'company', 'link']
    list_editable = relationship_list_editable + ['rtype', 'company', 'link']
    search_fields = relationship_list_search_fields + ['rtype', 'company',
        'link']

    # Details page settings
    fieldsets = relationship_fieldsets + [
        ('Model references', {'fields': ['rtype', 'company', 'link']})
    ]
    autocomplete_fields = ['rtype', 'company', 'link']

@admin.register(CompanyAddress)
class CompanyAddressAdmin(RelationshipAdmin):
    # List page settings
    list_display = relationship_list_display + ['rtype', 'company', 'address']
    list_editable = relationship_list_editable + ['rtype', 'company', 'address']
    search_fields = relationship_list_search_fields + ['rtype', 'company',
        'address']

    # Details page settings
    fieldsets = relationship_fieldsets + [
        ('Model references', {'fields': ['rtype', 'company', 'address']})
    ]
    autocomplete_fields = ['rtype', 'company', 'address']

@admin.register(CompanyPhoneNumber)
class CompanyPhoneNumberAdmin(RelationshipAdmin):
    # List page settings
    list_display = relationship_list_display + ['rtype', 'company',
        'phone_number']
    list_editable = relationship_list_editable + ['rtype', 'company',
        'phone_number']
    search_fields = relationship_list_search_fields + ['rtype', 'company',
        'phone_number']

    # Details page settings
    fieldsets = relationship_fieldsets + [
        ('Model references', {'fields': ['rtype', 'company', 'phone_number']})
    ]
    autocomplete_fields = ['rtype', 'company', 'phone_number']

@admin.register(CompanyEmail)
class CompanyEmailAdmin(RelationshipAdmin):
    # List page settings
    list_display = relationship_list_display + ['rtype', 'company', 'email']
    list_editable = relationship_list_editable + ['rtype', 'company', 'email']
    search_fields = relationship_list_search_fields + ['rtype', 'company',
        'email']

    # Details page settings
    fieldsets = relationship_fieldsets + [
        ('Model references', {'fields': ['rtype', 'company', 'email']})
    ]
    autocomplete_fields = ['rtype', 'company', 'email']