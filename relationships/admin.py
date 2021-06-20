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

_phone_number_hash_fields = ['user', 'phone_number_type', 'phone_number']
@admin.register(mod.PhoneNumberHash)
class PhoneNumberHashAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _phone_number_hash_fields
    list_editable = comadm.standard_list_editable + _phone_number_hash_fields
    list_filter = comadm.standard_list_filter + ['phone_number_type']
    search_fields = comadm.standard_search_fields + ['user__id',
        'phone_number__country_code', 'phone_number__national_number']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _phone_number_hash_fields})
    ]
    autocomplete_fields = ['user', 'phone_number']

_phone_number_link_access_fields = ['ip_address', 'is_mobile', 'is_tablet',
    'is_touch_capable', 'is_pc', 'is_bot', 'browser', 'browser_family',
    'browser_version', 'browser_version_string', 'os', 'os_version',
    'os_version_string', 'device', 'device_family', 'hash']
@admin.register(mod.PhoneNumberLinkAccess)
class PhoneNumberLinkAccessAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + \
        _phone_number_link_access_fields
    list_editable = comadm.standard_list_editable + \
        _phone_number_link_access_fields
    search_fields = comadm.standard_search_fields + ['ip_address',
        'browser', 'browser_family', 'browser_version_string', 'os',
        'os_version_string', 'device', 'device_family']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _phone_number_link_access_fields})
    ]

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

_supply_fields = ['quantity', 'price', 'deposit_percentage', 'accept_lc']
_supply_fk_fields = ['user', 'product_type', 'country', 'state', 'availability',
    'packing', 'pre_order_timeframe', 'currency', 'previous_version',
    'next_version']


_supply_fields = [ 'user', 'product_type_data_value', 'product_type_method',
'product_type', 'country_data_value', 'country_method', 'country',
'state_data_value', 'state_method', 'state', 'availability_data_value',
'availability_method', 'availability', 'packing_data_value', 'packing_method',
'packing', 'quantity_data_value', 'quantity_method', 'quantity',
'pre_order_timeframe_data_value', 'pre_order_timeframe_method',
'pre_order_timeframe', 'price_data_value', 'price_method', 'price',
'currency_data_value', 'currency_method', 'currency',
'deposit_percentage_data_value', 'deposit_percentage_method',
'deposit_percentage', 'accept_lc_data_value', 'accept_lc_method', 'accept_lc',
'previous_version', 'next_version']
@admin.register(mod.Supply)
class SupplyAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _supply_fields
    list_editable = comadm.standard_list_editable + _supply_fields
    list_filter = comadm.standard_list_filter + ['product_type', 'country',
    'state', 'availability', 'packing', 'accept_lc']
    search_fields = comadm.standard_search_fields + ['user__name']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _supply_fields})
    ]
    autocomplete_fields = [ 'user', 'product_type_data_value', 'product_type',
    'country_data_value', 'country', 'state_data_value', 'state',
    'availability_data_value', 'availability', 'packing_data_value', 'packing',
    'quantity_data_value', 'pre_order_timeframe_data_value',
    'pre_order_timeframe', 'price_data_value', 'currency_data_value',
    'currency', 'deposit_percentage_data_value', 'accept_lc_data_value',
    'previous_version', 'next_version']

_demand_fields = ['user', 'product_type_data_value', 'product_type_method',
'product_type', 'country_data_value', 'country_method', 'country',
'state_data_value', 'state_method', 'state', 'packing_data_value',
'packing_method', 'packing', 'quantity_data_value', 'quantity_method',
'quantity', 'price_data_value', 'price_method', 'price', 'currency_data_value',
'currency_method', 'currency', 'previous_version', 'next_version']
@admin.register(mod.Demand)
class DemandAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _demand_fields
    list_editable = comadm.standard_list_editable + _demand_fields
    list_filter = comadm.standard_list_filter + ['product_type', 'country',
    'state', 'packing']
    search_fields = comadm.standard_search_fields + ['user__name']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _demand_fields})
    ]
    autocomplete_fields = ['user', 'product_type_data_value', 'product_type',
    'country_data_value', 'country', 'state_data_value', 'state',
    'packing_data_value', 'packing', 'quantity_data_value', 'price_data_value',
    'currency_data_value', 'currency', 'previous_version', 'next_version']