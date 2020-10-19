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

class CompanyAdmin(admin.ModelAdmin):
    search_fields = ['id']

class PhoneNumberAdmin(admin.ModelAdmin):
    search_fields = ['id']

class EmailAdmin(admin.ModelAdmin):
    search_fields = ['id']

class PersonAdmin(admin.ModelAdmin):
    search_fields = ['id']

class LinkAdmin(admin.ModelAdmin):
    search_fields = ['id']

admin.site.register(PersonLink)
admin.site.register(PersonAddress)
admin.site.register(PersonPhoneNumber)
admin.site.register(PersonEmail)
admin.site.register(CompanyLink)
admin.site.register(CompanyAddress)
admin.site.register(CompanyPhoneNumber)
admin.site.register(CompanyEmail)
admin.site.register(Person, PersonAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Email, EmailAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(PhoneNumber, PhoneNumberAdmin)