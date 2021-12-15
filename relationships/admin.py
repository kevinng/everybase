from everybase.settings import BASE_URL
from urllib.parse import urljoin
from django.urls import reverse
from django.utils.html import format_html

from files.models import File
from django.contrib import admin

from . import models as mod
from common import admin as comadm
from growth import models as gromods

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

class GmassEmailStatusInlineAdmin(admin.TabularInline):
    model = gromods.GmassEmailStatus
    extra = 0
    autocomplete_fields = ['invalid_email']

class GmassCampaignResultInlineAdmin(admin.TabularInline):
    model = gromods.GmassCampaignResult
    extra = 0
    autocomplete_fields = ['import_job', 'invalid_email', 'gmass_campaign']

class ChemicalClusterOfSingaporeCompanyInlineAdmin(admin.TabularInline):
    model = gromods.ChemicalClusterOfSingaporeCompany
    fk_name = 'email'
    extra = 0
    autocomplete_fields = ['import_job', 'invalid_email', 'executive_email',
        'invalid_executive_email']

class Fibre2FashionBuyingOfferInlineAdmin(admin.TabularInline):
    model = gromods.Fibre2FashionBuyingOffer
    extra = 0
    autocomplete_fields = ['import_job', 'invalid_email']

class Fibre2FashionSellingOfferInlineAdmin(admin.TabularInline):
    model = gromods.Fibre2FashionSellingOffer
    extra = 0
    autocomplete_fields = ['import_job', 'invalid_email']

class ZeroBounceResultInlineAdmin(admin.TabularInline):
    model = gromods.ZeroBounceResult
    fk_name = 'email'
    extra = 0
    autocomplete_fields = ['import_job', 'invalid_email', 'did_you_mean_email']

class ZeroBounceResultDidYouMeanEmailInlineAdmin(admin.TabularInline):
    model = gromods.ZeroBounceResult
    fk_name = 'did_you_mean_email'
    extra = 0
    autocomplete_fields = ['import_job', 'invalid_email', 'did_you_mean_email']

class ChemicalBookSupplierInlineAdmin(admin.TabularInline):
    model = gromods.ChemicalBookSupplier
    extra = 0
    autocomplete_fields = ['import_job', 'invalid_email']

class LookChemSupplierInlineAdmin(admin.TabularInline):
    model = gromods.LookChemSupplier
    extra = 0
    autocomplete_fields = ['import_job', 'invalid_email']

class WorldOfChemicalsSupplierInlineAdmin(admin.TabularInline):
    model = gromods.WorldOfChemicalsSupplier
    fk_name = 'email'
    extra = 0
    autocomplete_fields = ['import_job', 'owner_email', 'alt_email',
        'alt_email_2', 'alt_email_3', 'invalid_email', 'invalid_owner_email',
        'invalid_alt_email', 'invalid_alt_email_2', 'invalid_alt_email_3']

class EmailStatusInlineAdmin(admin.TabularInline):
    model = gromods.EmailStatus.emails.through
    extra = 1
    autocomplete_fields = ['emailstatus']

_email_fields = ['user', 'verified', 'email', 'notes', 'invalid_email',
    'import_job']
@admin.register(mod.Email)
class EmailAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _email_fields
    list_editable = comadm.standard_list_editable + ['email', 'notes']
    list_filter = comadm.standard_list_filter + ['import_job']
    search_fields = comadm.standard_search_fields + ['email']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _email_fields})
    ]
    autocomplete_fields = ['import_job', 'invalid_email']
    inlines = [
        EmailStatusInlineAdmin
        # GmassEmailStatusInlineAdmin,
        # GmassCampaignResultInlineAdmin,
        # ChemicalClusterOfSingaporeCompanyInlineAdmin,
        # Fibre2FashionBuyingOfferInlineAdmin,
        # Fibre2FashionSellingOfferInlineAdmin,
        # ZeroBounceResultInlineAdmin,
        # ZeroBounceResultDidYouMeanEmailInlineAdmin,
        # ChemicalBookSupplierInlineAdmin,
        # LookChemSupplierInlineAdmin,
        # WorldOfChemicalsSupplierInlineAdmin
    ]

class EmailInlineAdmin(admin.TabularInline):
    model = mod.Email
    extra = 1
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
    inlines = [EmailInlineAdmin]

_user_fields = ['registered', 'django_user', 'first_name', 'last_name',
    'languages_string', 'country', 'state', 'state_string', 'phone_number',
    'email', 'is_direct_buyer', 'is_direct_seller', 'is_buying_agent',
    'is_selling_agent', 'internal_notes']
@admin.register(mod.User)
class UserAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _user_fields
    list_editable = comadm.standard_list_editable + _user_fields
    list_filter = comadm.standard_list_filter + ['registered',
        'is_direct_buyer', 'is_direct_seller', 'is_buying_agent',
        'is_selling_agent']
    search_fields = comadm.standard_search_fields + [
        'first_name', 'last_name', 'country__name', 'state__name',
        'state_string', 'phone_number__country_code',
        'phone_number__national_number', 'email__email', 'internal_notes']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _user_fields + ['languages']})
    ]
    autocomplete_fields = ['django_user', 'languages', 'country', 'state',
        'phone_number', 'email']

_phone_number_hash_fields = ['user', 'phone_number_type', 'phone_number']
@admin.register(mod.PhoneNumberHash)
class PhoneNumberHashAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['uuid'] + \
        _phone_number_hash_fields
    list_editable = comadm.standard_list_editable + _phone_number_hash_fields
    list_filter = comadm.standard_list_filter + ['phone_number_type']
    search_fields = comadm.standard_search_fields + ['user__id', 'uuid',
        'phone_number__country_code', 'phone_number__national_number']

    # Details page settings
    readonly_fields = comadm.standard_readonly_fields + ['uuid']
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': ['uuid'] + _phone_number_hash_fields})
    ]
    autocomplete_fields = ['user', 'phone_number']

# TODO: refactor to file module
class FileInlineAdmin(admin.TabularInline):
    model = File
    extra = 1
    fields = ['file_url', 'upload_confirmed', 's3_bucket_name',
        's3_object_key', 's3_object_content_length', 's3_object_e_tag',
        's3_object_content_type', 's3_object_last_modified']
    readonly_fields = ['uuid', 'file_url']

    def file_url(self, obj):
        if obj.id is None:
            return None

        url = urljoin(
            BASE_URL, reverse('files:get_file', args=[obj.uuid]))
        return format_html(f'<a href="{url}" target="{url}">{url}</a>')

_connection_fields = ['user_one', 'user_two']
@admin.register(mod.Connection)
class ConnectionAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + \
        _connection_fields
    list_editable = comadm.standard_list_editable + _connection_fields
    list_filter = comadm.standard_list_filter + ['created']
    search_fields = comadm.standard_search_fields + [
        'user_one__first_given_name', 'user_one__last_family_name',
        'user_two__first_given_name', 'user_two__last_family_name',
        'user_one__id', 'user_two__id']

    # Details page settings
    readonly_fields = comadm.standard_readonly_fields + ['created']
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': _connection_fields})
    ]
    autocomplete_fields = ['user_one', 'user_two']

_login_token_fields = ['user', 'activated', 'token', 'expiry_secs']
@admin.register(mod.LoginToken)
class LoginToken(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _login_token_fields
    list_editable = comadm.standard_list_editable + _login_token_fields
    list_filter = comadm.standard_list_filter + ['created']
    search_fields = comadm.standard_search_fields + ['token']

    # Details page settings
    readonly_fields = comadm.standard_readonly_fields + ['created']
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': _login_token_fields})
    ]
    autocomplete_fields = ['user']

_register_token_fields = ['user', 'activated', 'token', 'expiry_secs']
@admin.register(mod.RegisterToken)
class RegisterToken(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _register_token_fields
    list_editable = comadm.standard_list_editable + _register_token_fields
    list_filter = comadm.standard_list_filter + ['created']
    search_fields = comadm.standard_search_fields + ['token']

    # Details page settings
    readonly_fields = comadm.standard_readonly_fields + ['created']
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': _register_token_fields})
    ]
    autocomplete_fields = ['user']