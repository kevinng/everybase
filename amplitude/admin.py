from django.contrib import admin

from . import models as mod
from common import admin as comadm

_event_fields = ['requested', 'responded', 'response_code', 'response_text',
    'user_id', 'device_id', 'event_type', 'time_dt', 'time', 'app_version',
    'platform', 'os_name', 'os_version', 'device_brand', 'device_manufacturer',
    'device_model', 'carrier', 'country', 'region', 'city', 'dma', 'language',
    'price', 'quantity', 'revenue', 'product_id', 'revenue_type',
    'location_lat', 'location_lng', 'ip', 'idfa', 'idfv', 'adid', 'android_id',
    'event_id', 'session_id', 'insert_id']
@admin.register(mod.Event)
class EventAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _event_fields
    list_editable = comadm.standard_list_editable + _event_fields
    list_filter = comadm.standard_list_filter + ['event_type', 'time_dt',
        'app_version', 'platform', 'os_name', 'os_version', 'device_brand',
        'device_manufacturer', 'device_model', 'carrier', 'country', 'region',
        'city', 'dma', 'language', 'product_id', 'revenue_type', 'idfa', 'idfv',
        'adid', 'android_id']
    search_fields = comadm.standard_search_fields + ['user_id', 'device_id',
        'event_type', 'app_version', 'platform', 'os_name', 'os_version',
        'device_brand', 'device_manufacturer', 'device_model', 'carrier',
        'country', 'region', 'city', 'dma', 'language', 'product_id',
        'revenue_type', 'location_lat', 'location_lng', 'ip', 'idfa', 'idfv',
        'adid', 'android_id', 'event_id', 'session_id', 'insert_id']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _event_fields})
    ]

_event_property_fields = ['key', 'value', 'event']
@admin.register(mod.EventProperty)
class EventPropertyAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _event_property_fields
    list_editable = comadm.standard_list_editable + _event_property_fields
    list_filter = comadm.standard_list_filter + ['key']
    search_fields = comadm.standard_search_fields + ['key', 'value']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _event_property_fields})
    ]
    autocomplete_fields = ['event']

_user_property_fields = ['key', 'value', 'user']
@admin.register(mod.UserProperty)
class UserPropertyAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _user_property_fields
    list_editable = comadm.standard_list_editable + _user_property_fields
    list_filter = comadm.standard_list_filter + ['key']
    search_fields = comadm.standard_search_fields + ['key', 'value']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _user_property_fields})
    ]
    autocomplete_fields = ['user']

_session_fields = ['started', 'session_id', 'last_activity', 'user']
@admin.register(mod.Session)
class SessionAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _session_fields
    list_editable = comadm.standard_list_editable + _session_fields
    list_filter = comadm.standard_list_filter + ['started', 'last_activity']
    search_fields = comadm.standard_search_fields + ['session_id']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _session_fields})
    ]
    autocomplete_fields = ['user']