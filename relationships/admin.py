import random, string

from urllib.parse import urljoin

from everybase import settings

from django.utils.html import format_html
from django.contrib import admin

from relationships import models
from common import admin as comadm
from growth import models as gromods
from leads import models as lemods

from relationships.utilities.get_non_tracking_whatsapp_link import get_non_tracking_whatsapp_link

@admin.register(models.PhoneNumberType)
class PhoneNumberTypeAdmin(comadm.ChoiceAdmin):
    pass

_phone_number_fields = ['country_code', 'national_number']
@admin.register(models.PhoneNumber)
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

class UserInlineAdmin(admin.TabularInline):
    # model = gromods.EmailStatus.emails.through
    model = models.User
    extra = 1
    fields = ['user_link']
    readonly_fields = ['user_link']

    def user_link(self, obj):
        link = urljoin(settings.BASE_URL, settings.ADMIN_PATH)
        link += f'/relationships/user/{obj.id}/change'
        return format_html(f'<a href="{link}" target="{link}">{obj.first_name} {obj.last_name}</a>')

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
        ('Details', {'fields': ['email', 'do_not_email', 'import_job', 'invalid_email']}),
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

class EmailInlineAdmin(admin.TabularInline):
    model = models.Email
    extra = 1
    autocomplete_fields = ['import_job']

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

class ApplicationMessageInlineAdmin(admin.TabularInline):
    model = lemods.ApplicationMessage
    extra = 0
    fields = ['application_link', 'body', 'applicant_link', 'lead_author_link']
    readonly_fields = ['application_link', 'body', 'applicant_link', 'lead_author_link']

    def application_link(self, obj):
        link = urljoin(settings.BASE_URL, settings.ADMIN_PATH)
        link += f'/leads/application/{obj.application.id}/change'
        return format_html(f'<a href="{link}" target="{link}">{obj.application}</a>')
    
    def applicant_link(self, obj):
        link = urljoin(settings.BASE_URL, settings.ADMIN_PATH)
        link += f'/relationships/user/{obj.application.applicant.id}/change'
        return format_html(f'<a href="{link}" target="{link}">{obj.application.applicant.first_name} {obj.application.applicant.last_name}</a>')

    def lead_author_link(self, obj):
        link = urljoin(settings.BASE_URL, settings.ADMIN_PATH)
        link += f'/relationships/user/{obj.application.lead.author.id}/change'
        return format_html(f'<a href="{link}" target="{link}">{obj.application.lead.author.first_name} {obj.application.lead.author.last_name}</a>')

class LeadInlineAdmin(admin.TabularInline):
    model = lemods.Lead
    extra = 0
    fields = ['lead_link']
    readonly_fields = ['lead_link']

    def lead_link(self, obj):
        link = urljoin(settings.BASE_URL, settings.ADMIN_PATH)
        link += f'/leads/lead/{obj.id}/change'
        return format_html(f'<a href="{link}" target="{link}">{obj.headline}</a>')

@admin.register(models.User)
class UserAdmin(comadm.StandardAdmin):
    # List page settings
    list_per_page = 100
    list_display = ['id', 'full_name', 'country', 'email', 'whatsapp_phone_number', 'created', 'has_insights']
    list_editable = [] # Override to speed up loading
    list_filter = ['created', 'has_insights']
    search_fields = ['id', 'uuid', 'first_name', 'last_name', 'country__name', 'email__email', 'internal_notes']

    # Details page settings
    readonly_fields = comadm.standard_readonly_fields + ['uuid', 'whatsapp_phone_number', 'email_string', 'password_change_link', 'random_string_for_password', 'django_user_link']
    fieldsets = [
        (None, {'fields': ['id', 'uuid']}),
        ('Growth', {'fields': ['registered', 'django_user', 'whatsapp_phone_number', 'email_string', 'password_change_link', 'random_string_for_password', 'fb_profile', 'django_user_link', 'has_insights', 'internal_notes']}),
        ('Details', {'fields': ['first_name', 'last_name', 'email', 'phone_number', 'country']}),
        ('Timestamps', {'fields': ['created', 'updated', 'deleted']}),
        ('Not in use', {'fields': [
            'slug_link', 'slug_tokens',
            'impressions', 'clicks',
            'has_company', 'company_name', 'goods_string', 'buy_agent_details', 'sell_agent_details', 'logistics_agent_details',
            'is_buyer', 'is_seller', 'is_buy_agent', 'is_sell_agent', 'is_logistics_agent',
            'state', 'state_string', 'languages', 'languages_string'
        ]})
    ]
    autocomplete_fields = ['django_user', 'country', 'phone_number', 'email']
    inlines = [ApplicationMessageInlineAdmin, LeadInlineAdmin]

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

        link = get_non_tracking_whatsapp_link(
            obj.phone_number.country_code,
            obj.phone_number.national_number
        )
        return format_html(f'<a href="{link}" target="{link}">{obj.phone_number}</a>')

    def django_user_link(self, obj):
        if obj.django_user is None:
            return None

        link = urljoin(settings.BASE_URL, settings.ADMIN_PATH)
        link += f'/auth/user/{obj.django_user.id}/change'
        return format_html(f'<a href="{link}" target="{link}">{link}</a>')

_login_token_fields = ['user', 'activated', 'killed','token']
@admin.register(models.LoginToken)
class LoginTokenAdmin(comadm.StandardAdmin):
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

_register_token_fields = ['user', 'activated', 'killed', 'token']
@admin.register(models.RegisterToken)
class RegisterTokenAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _register_token_fields
    list_editable = comadm.standard_list_editable + _register_token_fields
    list_filter = comadm.standard_list_filter + ['created']
    search_fields = comadm.standard_search_fields + ['user__first_name',
        'user__last_name', 'token']

    # Details page settings
    readonly_fields = comadm.standard_readonly_fields + ['created']
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': _register_token_fields})
    ]
    autocomplete_fields = ['user']

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

_user_comment_fields = ['commentee', 'commentor', 'body']
@admin.register(models.UserComment)
class UserCommentAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _user_comment_fields
    list_editable = comadm.standard_list_editable + _user_comment_fields
    search_fields = comadm.standard_search_fields + ['commentee__first_name',
        'commentee__last_name', 'commentor__first_name', 'commentor__last_name',
        'body']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': _user_comment_fields})
    ]
    autocomplete_fields = ['commentee', 'commentor']

_user_detail_views_fields = ['viewee', 'viewer', 'comments_view_count',
    'leads_view_count']
@admin.register(models.UserDetailView)
class UserDetailViewAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _user_detail_views_fields
    list_editable = comadm.standard_list_editable + _user_detail_views_fields
    list_filter = comadm.standard_list_filter
    search_fields = comadm.standard_search_fields + ['viewee__first_name',
        'viewee__last_name', 'viewer__first_name', 'viewer__last_name']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': _user_detail_views_fields})
    ]
    autocomplete_fields = ['viewee', 'viewer']

_saved_user_fields = ['active', 'saver', 'savee']
@admin.register(models.SavedUser)
class SavedUserAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _saved_user_fields
    list_editable = comadm.standard_list_editable + _saved_user_fields
    list_filter = comadm.standard_list_filter + ['active']
    search_fields = comadm.standard_search_fields + ['saver__id',
        'saver__family_first_name', 'saver__family_last_name', 'savee__id',
        'savee__family_first_name', 'savee__family_last_name',]

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _saved_user_fields})]
    autocomplete_fields = ['saver', 'savee']

_user_query_fields = ['user', 'commented_only', 'saved_only', 'connected_only',
'first_name', 'last_name', 'company_name', 'country', 'goods_string',
'languages', 'is_buy_agent', 'buy_agent_details', 'is_sell_agent',
'sell_agent_details', 'is_logistics_agent', 'logistics_agent_details']
@admin.register(models.UserQuery)
class UserQueryAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _user_query_fields
    list_editable = comadm.standard_list_editable + _user_query_fields
    list_filter = comadm.standard_list_filter
    search_fields = comadm.standard_search_fields + ['user__id',
        'commented_only', 'saved_only', 'connected_only', 'first_name',
        'last_name', 'company_name', 'country', 'goods_string', 'languages',
        'is_buy_agent', 'buy_agent_details', 'is_sell_agent',
        'sell_agent_details', 'is_logistics_agent', 'logistics_agent_details']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [('Details', {'fields': _user_query_fields})]
    autocomplete_fields = ['user']