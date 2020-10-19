from django.contrib import admin
from .models import (PersonLinkType, PersonLink, PersonCompanyType,
    PersonAddressType, PersonAddress, PersonPhoneNumberType, PersonPhoneNumber,
    PersonEmailType, PersonEmail, CompanyLinkType, CompanyLink,
    CompanyAddressType, CompanyAddress, CompanyPhoneNumberType,
    CompanyPhoneNumber, CompanyEmailType, CompanyEmail, Person, Company, Email,
    LinkType, Link, AddressType, Address, PhoneNumberType, PhoneNumber)
from common.admin import (ChoiceAdmin)

@admin.register(PersonLinkType, PersonCompanyType, PersonAddressType,
    PersonPhoneNumberType, PersonEmailType, CompanyLinkType, CompanyAddressType,
    CompanyPhoneNumberType, CompanyEmailType, LinkType, AddressType,
    PhoneNumberType)
class ChoiceAdmin(ChoiceAdmin):
    pass

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

class AddressAdmin(admin.ModelAdmin):
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
admin.site.register(Address, AddressAdmin)
admin.site.register(PhoneNumber, PhoneNumberAdmin)