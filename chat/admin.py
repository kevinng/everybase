from django.contrib import admin

from . import models as mod
from common import admin as comadm

_message_template_fields = ['programmatic_key', 'is_active', 'internal_title',
    'notes', 'body']
@admin.register(mod.MessageTemplate)
class MessageTemplateAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _message_template_fields
    list_editable = comadm.standard_list_editable + _message_template_fields
    list_filter = comadm.standard_list_filter + ['is_active']
    search_fields = comadm.standard_search_fields + ['programmatic_key',
        'internal_title', 'notes', 'body']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _message_template_fields})
    ]

_twilio_outbound_message_fields = ['message_template', 'date_created',
    'date_sent', 'direction', 'account_sid', 'message_sid', 'from_str',
    'to_str', 'body', 'uri', 'error_message', 'error_code', 'api_version',
    'from_user', 'to_user', 'twilml_response_to']
@admin.register(mod.TwilioOutboundMessage)
class TwilioOutboundMessage(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + \
        _twilio_outbound_message_fields
    list_editable = comadm.standard_list_editable + \
        _twilio_outbound_message_fields
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['message_template',
        'date_created', 'date_sent', 'direction', 'error_message', 'error_code',
        'api_version']
    search_fields = comadm.standard_search_fields + [
        'message_template__programmatic_key',
        'message_template__internal_title', 'notes', 'body', 'direction',
        'account_sid', 'message_sid', 'from_str', 'to_str', 'uri',
        'error_message', 'error_code', 'api_version', 'from_user', 'to_user',
        'twilml_response_to__message_sid']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _twilio_outbound_message_fields})
    ]
    autocomplete_fields = ['message_template', 'from_user', 'to_user',
        'twilml_response_to']

_twilio_status_callback_fields = ['from_str', 'to_str', 'account_sid',
    'api_version', 'channel_to_address', 'channel_install_sid',
    'channel_status_message', 'channel_prefix', 'message_sid', 'message_status',
    'sms_sid', 'sms_status', 'error_code', 'event_type', 'message', 'log_entry']
@admin.register(mod.TwilioStatusCallback)
class TwilioStatusCallbackAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _twilio_status_callback_fields
    list_editable = comadm.standard_list_editable + \
        _twilio_status_callback_fields
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['api_version',
        'channel_status_message', 'channel_prefix', 'message_status',
        'error_code', 'event_type']
    search_fields = comadm.standard_search_fields + ['from_str', 'to_str',
        'account_sid', 'api_version', 'channel_to_address',
        'channel_install_sid', 'channel_status_message', 'channel_prefix',
        'message_sid', 'message_status', 'sms_sid', 'sms_status', 'error_code',
        'event_type', 'log_entry__payload']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _twilio_status_callback_fields})
    ]
    autocomplete_fields = ['message', 'log_entry']

@admin.register(mod.TwilioStatusCallbackLogEntry)
class TwilioStatusCallbackLogEntryAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['payload']
    list_editable = comadm.standard_list_editable + ['payload']
    list_per_page = 50
    list_filter = comadm.standard_list_filter
    search_fields = comadm.standard_search_fields + ['payload']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': ['payload']})
    ]

_twilio_inbound_message_request_fields = ['api_version',
    'message_sid', 'sms_sid', 'sms_message_sid', 'account_sid',
    'message_service_sid', 'from_str', 'to_str', 'body', 'num_media',
    'num_segments']
_twilio_inbound_message_geographic_fields = ['from_city', 'from_state',
    'from_zip', 'from_country', 'to_city', 'to_state', 'to_zip', 'to_country']
_twilio_inbound_message_whatsapp_fields = ['profile_name', 'wa_id', 'forwarded',
    'frequently_forwarded']
_twilio_inbound_message_whatsapp_location_fields = ['latitude', 'longitude',
    'address', 'label']
@admin.register(mod.TwilioInboundMessage)
class TwilioInboundMessage(admin.ModelAdmin):
        # List page settings
    list_display = comadm.standard_list_display + \
        _twilio_inbound_message_request_fields + \
        _twilio_inbound_message_geographic_fields + \
        _twilio_inbound_message_whatsapp_fields + \
        _twilio_inbound_message_whatsapp_location_fields
    list_editable = comadm.standard_list_editable + \
        _twilio_inbound_message_request_fields + \
        _twilio_inbound_message_geographic_fields + \
        _twilio_inbound_message_whatsapp_fields + \
        _twilio_inbound_message_whatsapp_location_fields
    list_per_page = 50
    list_filter = comadm.standard_list_filter
    search_fields = comadm.standard_search_fields + ['api_version',
        'message_sid', 'sms_sid', 'sms_message_sid', 'account_sid',
        'message_service_sid', 'from_str', 'to_str', 'body', 'from_city',
        'from_state', 'from_zip', 'from_country', 'to_city', 'to_state',
        'to_zip', 'to_country', 'profile_name', 'wa_id', 'address', 'label']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        ('Request Parameters',
            {'fields': _twilio_inbound_message_request_fields}),
        ('Geographic Data-Related Parameters',
            {'fields': _twilio_inbound_message_geographic_fields}),
        ('WhatsApp-Specific Parameters',
            {'fields': _twilio_inbound_message_whatsapp_fields}),
        ('WhatsApp Location-Sharing Parameters',
            {'fields': _twilio_inbound_message_whatsapp_location_fields})
    ]

_inbound_message_group_fields = ['is_disabled', 'grouped', 'initial_body']
@admin.register(mod.InboundMessageGroup)
class InboundMessageGroupAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _inbound_message_group_fields
    list_editable = comadm.standard_list_editable + \
        _inbound_message_group_fields
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['grouped']
    search_fields = comadm.standard_search_fields + ['initial_body']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _inbound_message_group_fields + \
            ['twilio_inbound_messages']})
    ]
    autocomplete_fields = ['twilio_inbound_messages']

_grouping_method_fields = ['applied', 'order', 'inbound_message_group',
    'method']
@admin.register(mod.GroupingMethod)
class GroupingMethodAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _grouping_method_fields
    list_editable = comadm.standard_list_editable + \
        _grouping_method_fields
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['applied', 'method']
    search_fields = comadm.standard_search_fields + [
        'inbound_message_group__initial_body', 'method__title']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _grouping_method_fields})
    ]
    autocomplete_fields = ['inbound_message_group', 'method']

_operation_method_fields = ['applied', 'order', 'output_body',
    'inbound_message_group', 'method']
@admin.register(mod.OperationMethod)
class OperationMethodAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _operation_method_fields
    list_editable = comadm.standard_list_editable + \
        _operation_method_fields
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['applied', 'method']
    search_fields = comadm.standard_search_fields + ['output_body',
        'inbound_message_group__initial_body', 'method__title']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _operation_method_fields})
    ]
    autocomplete_fields = ['inbound_message_group', 'method']

_method_fields = ['title', 'version']
@admin.register(mod.Method)
class MethodAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _method_fields
    list_editable = comadm.standard_list_editable + \
        _method_fields
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['tags']
    search_fields = comadm.standard_search_fields + ['title', 'version']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _grouping_method_fields + ['tags']})
    ]
    autocomplete_fields = ['tags']

@admin.register(mod.MethodTag)
class MethodTagAdmin(comadm.ChoiceAdmin):
    pass

_inbound_message_group_relationship_fields = ['associated', 'group']
_inbound_message_group_relationship_m2m_fields = ['tags', 'supplies', 'demands',
    'supply_quotes', 'demand_quotes']
@admin.register(mod.InboundMessageGroupRelationship)
class InboundMessageGroupRelationshipAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + \
        _inbound_message_group_relationship_fields
    list_editable = comadm.standard_list_editable + \
        _inbound_message_group_relationship_fields
    list_per_page = 50
    list_filter = comadm.standard_list_filter + \
        _inbound_message_group_relationship_fields + \
        _inbound_message_group_relationship_m2m_fields
    search_fields = comadm.standard_search_fields + ['group__initial_body']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _inbound_message_group_relationship_fields +\
            _inbound_message_group_relationship_m2m_fields})
    ]
    autocomplete_fields = _inbound_message_group_relationship_m2m_fields

@admin.register(mod.InboundMessageGroupRelationshipTag)
class InboundMessageGroupRelationshipTagAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_choice_list_display
    list_editable = comadm.standard_choice_list_editable
    list_per_page = 50
    list_filter = comadm.standard_choice_list_filter
    search_fields = comadm.standard_choice_search_fields
    ordering = comadm.standard_choice_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_choice_readonly_fields
    fieldsets = comadm.standard_choice_fieldsets