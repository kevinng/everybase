from django.contrib import admin

from . import models as mod
from common import admin as comadm

@admin.register(
    mod.PersonLinkType,
    mod.PersonCompanyType,
    mod.PersonAddressType,
    mod.PersonPhoneNumberType,
    mod.PersonEmailType,
    mod.CompanyLinkType,
    mod.CompanyAddressType,
    mod.CompanyPhoneNumberType,
    mod.CompanyEmailType,
    mod.PhoneNumberType)
class ChoiceAdmin(comadm.ChoiceAdmin):
    pass

_address_fields = ['address_1', 'address_2', 'address_3', 'country',
    'state', 'postal_code']
@admin.register(mod.Address)
class AddressAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _address_fields
    list_editable = comadm.standard_list_editable + _address_fields
    list_per_page = 1000
    list_filter = comadm.standard_list_filter + ['country', 'state']
    search_fields = ['id'] + _address_fields
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + \
        [(None, {'fields': _address_fields})]
    autocomplete_fields = ['country', 'state']

_company_fields = ['company_name', 'company_name_wo_postfix', 'notes_md']
@admin.register(mod.Company)
class CompanyAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _company_fields
    list_editable = comadm.standard_list_editable + _company_fields
    list_per_page = 1000
    list_filter = comadm.standard_list_filter
    search_fields = ['id'] + _company_fields
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + \
        [(None, {'fields': _company_fields})]

_phone_number_fields = ['country_code', 'national_number']
@admin.register(mod.PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _phone_number_fields
    list_editable = comadm.standard_list_editable + _phone_number_fields
    list_per_page = 1000
    list_filter = comadm.standard_list_filter + ['country_code']
    search_fields = ['id'] + _phone_number_fields
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + \
        [(None, {'fields': _phone_number_fields})]

@admin.register(mod.Email)
class EmailAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['email', 'import_job']
    list_editable = comadm.standard_list_editable + ['email', 'import_job']
    list_per_page = 1000
    list_filter = comadm.standard_list_filter + ['import_job']
    search_fields = ['id', 'email', 'import_job']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': ['email', 'import_job']})
    ]
    autocomplete_fields = ['import_job']

@admin.register(mod.InvalidEmail)
class InvalidEmailAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['email', 'import_job']
    list_editable = comadm.standard_list_editable + ['email', 'import_job']
    list_per_page = 1000
    list_filter = comadm.standard_list_filter + ['import_job']
    search_fields = ['id', 'email', 'import_job']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': ['email', 'import_job']})
    ]
    autocomplete_fields = ['import_job']

_person_fields = ['given_name', 'family_name', 'country', 'state', 'notes_md']
@admin.register(mod.Person)
class PersonAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _person_fields
    list_editable = comadm.standard_list_editable + _person_fields
    list_per_page = 1000
    list_filter = comadm.standard_list_filter
    search_fields = ['id'] + _person_fields
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + \
        [(None, {'fields': _person_fields})]
    autocomplete_fields = ['country', 'state']

_link_fields = ['verified', 'link']
@admin.register(mod.Link)
class LinkAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _link_fields
    list_editable = comadm.standard_list_editable + _link_fields
    list_per_page = 1000
    list_filter = comadm.standard_list_filter
    search_fields = ['id', 'link']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + \
        [(None, {'fields': _link_fields})]

# --- Start: Relationships ---

_rel_list_display = comadm.standard_list_display + ['details_md', 'rtype']
_prel_list_display = _rel_list_display + ['person']
_crel_list_display = _rel_list_display + ['company']

_rel_list_editable = comadm.standard_list_editable + ['details_md', 'rtype']
_prel_list_editable = _rel_list_editable + ['person']
_crel_list_editable = _rel_list_editable + ['company']

_rel_list_search_fields = ['id', 'details_md', 'rtype']
_prel_list_search_fields = _rel_list_search_fields + ['person']
_crel_list_search_fields = _rel_list_search_fields + ['company']

_rel_fieldsets_fields = ['details_md', 'rtype']
_prel_fieldsets = lambda field: comadm.standard_fieldsets + [
    (None, {'fields': _rel_fieldsets_fields + ['person', field]})]
_crel_fieldsets = lambda field: comadm.standard_fieldsets + [
    (None, {'fields': _rel_fieldsets_fields + ['company', field]})]

_rel_autocomplete_fields = ['rtype']
_prel_autocomplete_fields = _rel_autocomplete_fields + ['person']
_crel_autocomplete_fields = _rel_autocomplete_fields + ['company']

class RelationshipAdmin(admin.ModelAdmin):
    # List page settings
    list_per_page = 1000
    list_filter = comadm.standard_list_filter
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields

@admin.register(mod.PersonLink)
class PersonLinkAdmin(RelationshipAdmin):
    # List page settings
    list_display = _prel_list_display + ['link']
    list_editable = _prel_list_editable + ['link']
    search_fields = _prel_list_search_fields + ['link']

    # Details page settings
    fieldsets = _prel_fieldsets('link')
    autocomplete_fields = _prel_autocomplete_fields + ['link']

@admin.register(mod.PersonCompany)
class PersonCompanyAdmin(RelationshipAdmin):
    # List page settings
    list_display = _prel_list_display + ['company']
    list_editable = _prel_list_editable + ['company']
    search_fields = _prel_list_search_fields + ['company']

    # Details page settings
    fieldsets = _prel_fieldsets('company')
    autocomplete_fields = _prel_autocomplete_fields + ['company']

@admin.register(mod.PersonAddress)
class PersonAddressAdmin(RelationshipAdmin):
    # List page settings
    list_display = _prel_list_display + ['address']
    list_editable = _prel_list_editable + ['address']
    search_fields = _prel_list_search_fields + ['address']

    # Details page settings
    fieldsets = _prel_fieldsets('address')
    autocomplete_fields = _prel_autocomplete_fields + ['address']

@admin.register(mod.PersonPhoneNumber)
class PersonPhoneNumberAdmin(RelationshipAdmin):
    # List page settings
    list_display = _prel_list_display + ['phone_number']
    list_editable = _prel_list_editable + ['phone_number']
    search_fields = _prel_list_search_fields + ['phone_number']

    # Details page settings
    fieldsets = _prel_fieldsets('phone_number')
    autocomplete_fields = _prel_autocomplete_fields + ['phone_number']

@admin.register(mod.PersonEmail)
class PersonEmailAdmin(RelationshipAdmin):
    # List page settings
    list_display = _prel_list_display + ['email']
    list_editable = _prel_list_editable + ['email']
    search_fields = _prel_list_search_fields + ['email']

    # Details page settings
    fieldsets = _prel_fieldsets('email')
    autocomplete_fields = _prel_autocomplete_fields + ['email']

@admin.register(mod.CompanyLink)
class CompanyLinkAdmin(RelationshipAdmin):
    # List page settings
    list_display = _crel_list_display + ['link']
    list_editable = _crel_list_editable + ['link']
    search_fields = _crel_list_search_fields + ['link']

    # Details page settings
    fieldsets = _crel_fieldsets('link')
    autocomplete_fields = _crel_autocomplete_fields + ['link']

@admin.register(mod.CompanyAddress)
class CompanyAddressAdmin(RelationshipAdmin):
    # List page settings
    list_display = _crel_list_display + ['address']
    list_editable = _crel_list_editable + ['address']
    search_fields = _crel_list_search_fields + ['address']

    # Details page settings
    fieldsets = _crel_fieldsets('address')
    autocomplete_fields = _crel_autocomplete_fields + ['address']

@admin.register(mod.CompanyPhoneNumber)
class CompanyPhoneNumberAdmin(RelationshipAdmin):
    # List page settings
    list_display = _crel_list_display + ['phone_number']
    list_editable = _crel_list_editable + ['phone_number']
    search_fields = _crel_list_search_fields + ['phone_number']

    # Details page settings
    fieldsets = _crel_fieldsets('phone_number')
    autocomplete_fields = _crel_autocomplete_fields + ['phone_number']

@admin.register(mod.CompanyEmail)
class CompanyEmailAdmin(RelationshipAdmin):
    # List page settings
    list_display = _crel_list_display + ['email']
    list_editable = _crel_list_editable + ['email']
    search_fields = _crel_list_search_fields + ['email']

    # Details page settings
    fieldsets = _crel_fieldsets('email')
    autocomplete_fields = _crel_autocomplete_fields + ['email']

# --- End: Relationships ---