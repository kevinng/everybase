import random, string
from urllib.parse import urljoin
from everybase import settings
from django.utils.html import format_html
from django.contrib import admin
from relationships import models
from common import admin as comadm
from growth import models as gromods

from relationships.utilities.get_whatsapp_url import get_whatsapp_url

# Inlines

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

class UserInlineAdmin(admin.TabularInline):
    model = models.User
    extra = 1
    fields = ['user_link']
    readonly_fields = ['user_link']
    fk_name = 'email'

    def user_link(self, obj):
        link = urljoin(settings.BASE_URL, settings.ADMIN_PATH)
        link += f'/relationships/user/{obj.id}/change'
        return format_html(f'<a href="{link}" target="{link}">{obj.first_name}\
 {obj.last_name}</a>')

class EmailInlineAdmin(admin.TabularInline):
    model = models.Email
    extra = 1
    autocomplete_fields = ['import_job']

# General

@admin.register(models.PhoneNumberType)
class PhoneNumberTypeAdmin(comadm.ChoiceAdmin):
    pass

_phone_number_fields = ['country_code', 'national_number']
@admin.register(models.PhoneNumber)
class PhoneNumberAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _phone_number_fields
    list_editable = [] # Speed up loading
    list_filter = comadm.standard_list_filter + ['country_code']
    search_fields = comadm.standard_search_fields + _phone_number_fields

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _phone_number_fields + ['types']})]
    autocomplete_fields = ['types']

_email_fields = ['verified', 'email', 'notes', 'invalid_email', 'import_job']
@admin.register(models.Email)
class EmailAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _email_fields
    list_display = ['id', 'created', 'email', 'do_not_email', 'import_job']
    list_editable = ['do_not_email'] # Override to speed up loading
    list_filter = ['do_not_email', 'import_job']
    search_fields = ['id', 'email']

    # Details page settings
    fieldsets = [
        (None, {'fields': ['id']}),
        ('Details', {'fields': ['email', 'do_not_email', 'import_job',
            'invalid_email']}),
        ('Timestamps', {'fields': ['created', 'updated', 'deleted']})
    ]
    autocomplete_fields = ['import_job', 'invalid_email']
    inlines = [
        UserInlineAdmin
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

_invalid_email_fields = ['email', 'import_job']
@admin.register(models.InvalidEmail)
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

@admin.register(models.User)
class UserAdmin(comadm.StandardAdmin):
    # List page settings
    list_per_page = 100
    list_display = ['id', 'updated', 'full_name', 'country', 'email',
        'whatsapp_phone_number', 'created', 'has_insights', 'registered']
    list_editable = [] # Override to speed up loading
    list_filter = ['created', 'has_insights', 'registered']
    search_fields = ['id', 'first_name', 'last_name', 'country__name',
        'email__email', 'internal_notes']

    # Details page settings
    readonly_fields = comadm.standard_readonly_fields + [
        'whatsapp_phone_number', 'email_string', 'password_change_link',
        'random_string_for_password', 'django_user_link']
    fieldsets = [
        (None, {'fields': ['id']}),
        ('Growth', {'fields': ['registered', 'django_user',
            'whatsapp_phone_number', 'email_string',
            'password_change_link', 'random_string_for_password',
            'django_user_link', 'has_insights', 'internal_notes']}),
        ('Details', {'fields': ['email', 'first_name', 'last_name',
            'phone_number', 'country', 'business_name', 'business_address',
            'business_description', 'status', 'walked_through_status']}),
        ('Administration', {'fields': ['email_code_used', 'email_code',
            'email_code_generated', 'email_code_purpose','whatsapp_code_used',
            'whatsapp_code', 'whatsapp_code_generated', 'whatsapp_code_purpose',
            'pending_email'
            ]}),
        ('Timestamps', {'fields': ['created', 'updated', 'deleted']})
    ]
    autocomplete_fields = ['django_user', 'country', 'phone_number', 'email']
    # inlines = [LeadInlineAdmin]

    def full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'

    def password_change_link(self, obj):
        if obj.django_user is None:
            return None

        link = urljoin(settings.BASE_URL, settings.ADMIN_PATH)
        link += f'/auth/user/{obj.django_user.id}/password'
        return format_html(f'<a href="{link}" target="{link}">{link}</a>')

    def random_string_for_password(self, obj):
        choices = string.ascii_lowercase + string.digits
        password_length = 8
        return ''.join(random.choice(choices) for i in range(password_length))

    def email_string(self, obj):
        if obj.email is None:
            return None

        return obj.email.email

    def whatsapp_phone_number(self, obj):
        if obj.phone_number is None:
            return None

        link = get_whatsapp_url(
            obj.phone_number.country_code,
            obj.phone_number.national_number
        )
        return format_html(
            f'<a href="{link}" target="{link}">{obj.phone_number}</a>')

    def django_user_link(self, obj):
        if obj.django_user is None:
            return None

        link = urljoin(settings.BASE_URL, settings.ADMIN_PATH)
        link += f'/auth/user/{obj.django_user.id}/change'
        return format_html(f'<a href="{link}" target="{link}">{link}</a>')

_user_agent_fields = ['user', 'ip_address', 'is_routable', 'is_mobile',
    'is_tablet', 'is_touch_capable', 'is_pc', 'is_bot', 'browser',
    'browser_family', 'browser_version', 'browser_version_string',
    'os', 'os_family', 'os_version', 'os_version_string', 'device',
    'device_family']
@admin.register(models.UserAgent)
class UserAgentAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _user_agent_fields
    list_editable = comadm.standard_list_editable + _user_agent_fields
    list_filter = comadm.standard_list_filter + ['ip_address', 'is_routable',
        'is_mobile', 'is_tablet', 'is_touch_capable', 'is_pc', 'is_bot',
        'browser', 'browser_family', 'browser_version',
        'browser_version_string', 'os', 'os_family', 'os_version',
        'os_version_string', 'device', 'device_family']
    search_fields = comadm.standard_search_fields + ['ip_address',
        'browser', 'browser_family', 'browser_version',
        'browser_version_string', 'os', 'os_family', 'os_version',
        'os_version_string', 'device', 'device_family']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': _user_agent_fields})
    ]
    autocomplete_fields = ['user']

_login_action_fields = ['user']
@admin.register(models.LoginAction)
class LoginActionAdmin(comadm.StandardAdmin):
    list_display = comadm.standard_list_display + _login_action_fields
    list_editable = [] # Speed up loading
    search_fields = comadm.standard_search_fields + ['user__first_name',
        'user__last_name']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': _login_action_fields})
    ]
    autocomplete_fields = ['user']

_user_contact_action_fields = ['contactor', 'phone_number']
@admin.register(models.ContactAction)
class ContactActionAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _user_contact_action_fields
    list_editable = [] # Speed up loading
    list_filter = comadm.standard_list_filter
    search_fields = comadm.standard_search_fields + ['contactor__first_name',
        'contactor__last_name', 'phone_number__national_number']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': _user_contact_action_fields})
    ]
    autocomplete_fields = ['contactor', 'phone_number']

_user_detail_views_fields = ['viewee', 'viewer', 'count']
@admin.register(models.DetailView)
class DetailViewAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _user_detail_views_fields
    list_editable = [] # Speed up loading
    list_filter = comadm.standard_list_filter
    search_fields = comadm.standard_search_fields + ['viewee__first_name',
        'viewee__last_name', 'viewer__first_name', 'viewer__last_name']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': _user_detail_views_fields})
    ]
    autocomplete_fields = ['viewee', 'viewer']

_review_fields = ['reviewer', 'phone_number', 'rating', 'body']
@admin.register(models.Review)
class ReviewAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _review_fields
    list_editable = [] # Speed up loading
    list_filter = comadm.standard_list_filter + ['rating']
    search_fields = comadm.standard_search_fields + ['reviewer__first_name',
        'reviewer__last_name', 'body']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': _review_fields})
    ]
    autocomplete_fields = ['reviewer', 'phone_number']

_review_file_fields = ['form_uuid', 'activated', 'file_uuid', 'file',
    'phone_number', 'reviewer']
@admin.register(models.ReviewFile)
class ReviewFileAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _review_file_fields
    list_editable = [] # Speed up loading

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': _review_file_fields})
    ]
    autocomplete_fields = ['file', 'phone_number', 'reviewer']

_review_response_fields = ['review', 'author']
@admin.register(models.ReviewComment)
class ReviewCommentAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _review_response_fields
    list_editable = [] # Speed up loading
    search_fields = comadm.standard_search_fields + ['review__body',
        'author__first_name', 'author__last_name']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': _review_response_fields})
    ]

_status_file_fields = ['form_uuid', 'activated', 'user', 'file_uuid',
    'file']
@admin.register(models.StatusFile)
class StatusFileAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _status_file_fields
    list_editable = [] # Speed up loading
    search_fields = comadm.standard_search_fields + ['form_uuid',
        'file_uuid']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': _status_file_fields})
    ]
    autocomplete_fields = ['user', 'file']