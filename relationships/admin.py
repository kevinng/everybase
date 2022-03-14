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

_email_fields = ['verified', 'email', 'notes', 'invalid_email', 'import_job']
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

_user_fields = ['registered', 'django_user',

    'first_name', 'last_name', 'has_company', 'company_name',

    'goods_string', 'languages_string', 'country', 'state_string',
    'phone_number', 'email', 'internal_notes',

    'is_buy_agent', 'is_sell_agent', 'is_logistics_agent',

    'buy_agent_details', 'sell_agent_details', 'logistics_agent_details',

    'slug_link', 'slug_tokens',

    'search_appearance_count', 'search_to_user_count', 'saved_count',
    'state']
@admin.register(mod.User)
class UserAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['uuid'] + _user_fields
    list_editable = comadm.standard_list_editable + _user_fields
    list_filter = comadm.standard_list_filter + ['registered', 'has_company',
        'is_buy_agent', 'is_sell_agent', 'is_logistics_agent']
    search_fields = comadm.standard_search_fields + [
        'first_name', 'last_name', 'company_name', 'goods_string',
        'languages_string', 'country__name', 'state_string', 'email__email',
        'phone_number__country_code', 'phone_number__national_number',
        'internal_notes', 'buy_agent_details', 'sell_agent_details',
        'logistics_agent_details']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _user_fields + ['languages']})
    ]
    autocomplete_fields = ['django_user', 'languages', 'country', 'state',
        'phone_number', 'email']

_login_token_fields = ['user', 'activated', 'killed','token']
@admin.register(mod.LoginToken)
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
@admin.register(mod.RegisterToken)
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
@admin.register(mod.UserAgent)
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
@admin.register(mod.UserComment)
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
@admin.register(mod.UserDetailView)
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
@admin.register(mod.SavedUser)
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
@admin.register(mod.UserQuery)
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