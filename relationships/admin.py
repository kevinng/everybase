from django.contrib import admin

from . import models as mod
from common import admin as comadm

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

_email_fields = ['email', 'import_job']
@admin.register(mod.Email)
class EmailAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _email_fields
    list_editable = comadm.standard_list_editable + ['email']
    list_filter = comadm.standard_list_filter + ['import_job']
    search_fields = comadm.standard_search_fields + ['email']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _email_fields})
    ]
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

_user_fields = ['phone_number', 'name', 'is_banned', 'notes', 'email']
@admin.register(mod.User)
class UserAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['key'] + _user_fields
    list_editable = comadm.standard_list_editable + _user_fields
    list_filter = comadm.standard_list_filter + ['is_banned']
    search_fields = comadm.standard_search_fields + _user_fields

    # Details page settings
    readonly_fields = comadm.standard_readonly_fields + ['key']
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': ['key'] + _user_fields})
    ]
    autocomplete_fields = ['phone_number', 'email']

_accessed_url_fields = ['user', 'first_accessed', 'last_accessed', 'url',
    'count']
@admin.register(mod.AccessedURL)
class AccessedURLAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _accessed_url_fields
    list_editable = comadm.standard_list_editable + _accessed_url_fields
    list_filter = comadm.standard_list_filter + ['first_accessed',
        'last_accessed']
    search_fields = comadm.standard_search_fields + ['user__id', 'url']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _accessed_url_fields})
    ]
    autocomplete_fields = ['user']

_user_ip_device_fields = ['user', 'first_accessed', 'last_accessed', 'count',
    'ip_address', 'is_mobile', 'is_tablet', 'is_touch_capable', 'is_pc',
    'is_bot', 'browser', 'browser_family', 'browser_version',
    'browser_version_string', 'os', 'os_version', 'os_version_string', 'device',
    'device_family']
@admin.register(mod.UserIPDevice)
class UserIPDeviceAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _user_ip_device_fields
    list_editable = comadm.standard_list_editable + _user_ip_device_fields
    search_fields = comadm.standard_search_fields + ['user__id', 'ip_address',
        'browser', 'browser_family', 'browser_version_string', 'os',
        'os_version_string', 'device', 'device_family']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _user_ip_device_fields + ['accessed_urls']})
    ]
    autocomplete_fields = ['user', 'accessed_urls']

_unit_of_measure_fields = ['plural_name', 'product_type', 'priority']
@admin.register(mod.UnitOfMeasure)
class UnitOfMeasureAdmin(comadm.StandardChoiceAdmin):
    # List page settings
    list_display = comadm.standard_choice_list_display + _unit_of_measure_fields
    list_editable = comadm.standard_choice_list_editable + \
        _unit_of_measure_fields
    list_filter = comadm.standard_choice_list_filter + _unit_of_measure_fields
    search_fields = comadm.standard_choice_search_fields + \
        ['plural_name', 'product_type__name']

    # Details page settings
    fieldsets = comadm.standard_choice_fieldsets + [
        ('Details', {'fields': _unit_of_measure_fields})
    ]
    autocomplete_fields = ['product_type']

@admin.register(mod.Availability)
class AvailabilityAdmin(comadm.ChoiceAdmin):
    pass

@admin.register(mod.ProductType)
class ProductTypeAdmin(comadm.ChoiceAdmin):
    pass

_connection_fields = ['user_1', 'user_2']
@admin.register(mod.Connection)
class ConnectionAdmin(comadm.ChoiceAdmin):
    # List page settings
    list_display = comadm.choice_list_display + _connection_fields
    list_editable = comadm.choice_list_editable + _connection_fields
    list_filter = _connection_fields
    search_fields = comadm.choice_search_fields + ['user_1__name',
        'user_2__name']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _connection_fields})
    ]
    autocomplete_fields = _connection_fields

_time_frame_fields = ['duration_uom', 'duration', 'deadline']
@admin.register(mod.TimeFrame)
class TimeFrameAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _time_frame_fields
    list_editable = comadm.standard_list_editable + _time_frame_fields

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _time_frame_fields})
    ]

_match_fields = ['supply', 'demand']
@admin.register(mod.Match)
class MatchAdmin(comadm.ChoiceAdmin):
    # List page settings
    list_display = comadm.choice_list_display + _match_fields
    list_editable = comadm.choice_list_editable + _match_fields
    list_filter = _match_fields
    search_fields = ['supply__product_type__name', 'demand__product_type__name']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _match_fields})
    ]
    autocomplete_fields = _match_fields

_supply_fields = ['product_type_captured', 'country_state_captured',
    'availability_captured', 'packing_captured', 'quantity_captured',
    'quantity', 'pre_order_timeframe_captured', 'price_captured', 'price', 
    'deposit_percentage_captured', 'deposit_percentage',
    'accept_lc_captured', 'accept_lc']
_supply_fk_fields = ['user', 'product_type', 'country', 'state', 'availability',
    'packing', 'pre_order_timeframe', 'currency', 'previous_version',
    'next_version']
@admin.register(mod.Supply)
class SupplyAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _supply_fields + \
        _supply_fk_fields
    list_editable = comadm.standard_list_editable + _supply_fields + \
        _supply_fk_fields
    list_filter = comadm.standard_list_filter + _supply_fk_fields
    search_fields = comadm.standard_search_fields + _supply_fields + \
        ['user__name']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _supply_fields + _supply_fk_fields})
    ]
    autocomplete_fields = _supply_fk_fields

_demand_fields = ['product_type_captured', 'country_state_captured', 
    'packing_captured', 'quantity_captured', 'price_captured', 'price']
_demand_fk_fields = ['user', 'product_type', 'country', 'state',  'packing',
    'currency', 'previous_version', 'next_version']
@admin.register(mod.Demand)
class DemandAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _demand_fields + \
        _demand_fk_fields
    list_editable = comadm.standard_list_editable + _demand_fields + \
        _demand_fk_fields
    list_filter = comadm.standard_list_filter + _demand_fk_fields
    search_fields = comadm.standard_search_fields + _demand_fields + \
        ['user__name']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _demand_fields + _demand_fk_fields})
    ]
    autocomplete_fields = _demand_fk_fields