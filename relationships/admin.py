from django.contrib import admin
from .models import (PersonLinkType, PersonLink, PersonCompanyType,
    PersonAddressType, PersonAddress, PersonPhoneNumberType, PersonPhoneNumber,
    PersonEmailType, PersonEmail, CompanyLinkType, CompanyLink,
    CompanyAddressType, CompanyAddress, CompanyPhoneNumberType,
    CompanyPhoneNumber, CompanyEmailType, CompanyEmail, Person, Company, Email,
    LinkType, Link, AddressType, Address, PhoneNumberType, PhoneNumber)

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

admin.site.register(PersonLinkType)
admin.site.register(PersonLink)
admin.site.register(PersonCompanyType)
admin.site.register(PersonAddressType)
admin.site.register(PersonAddress)
admin.site.register(PersonPhoneNumberType)
admin.site.register(PersonPhoneNumber)
admin.site.register(PersonEmailType)
admin.site.register(PersonEmail)
admin.site.register(CompanyLinkType)
admin.site.register(CompanyLink)
admin.site.register(CompanyAddressType)
admin.site.register(CompanyAddress)
admin.site.register(CompanyPhoneNumberType)
admin.site.register(CompanyPhoneNumber)
admin.site.register(CompanyEmailType)
admin.site.register(CompanyEmail)
admin.site.register(Person, PersonAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Email, EmailAdmin)
admin.site.register(LinkType)
admin.site.register(Link, LinkAdmin)
admin.site.register(AddressType)
admin.site.register(Address, AddressAdmin)
admin.site.register(PhoneNumberType)
admin.site.register(PhoneNumber, PhoneNumberAdmin)