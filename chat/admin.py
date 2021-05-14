from django.contrib import admin

from . import models as mod
from common import admin as comadm

_message_template_fields = ['chat_context_type']
@admin.register(mod.MessageTemplate)
class MessageTemplateAdmin(comadm.StandardChoiceAdmin):
    # List page settings
    list_display = comadm.standard_choice_list_display + \
        _message_template_fields
    list_editable = comadm.standard_choice_list_editable + \
        _message_template_fields
    list_filter = comadm.standard_choice_list_filter + \
        _message_template_fields

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _message_template_fields})
    ]

_twilio_outbound_message_fields = ['message_template', 'date_created',
    'date_sent', 'direction', 'account_sid', 'message_sid', 'from_str',
    'to_str', 'body', 'uri', 'error_message', 'error_code', 'api_version',
    'from_user', 'to_user', 'twilml_response_to']
@admin.register(mod.TwilioOutboundMessage)
class TwilioOutboundMessage(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + \
        _twilio_outbound_message_fields
    list_editable = comadm.standard_list_editable + \
        _twilio_outbound_message_fields
    list_filter = comadm.standard_list_filter + ['message_template',
        'date_created', 'date_sent', 'direction', 'error_message', 'error_code',
        'api_version']
    search_fields = comadm.standard_search_fields + [
        'message_template__programmatic_key',
        'message_template__internal_title', 'notes', 'body', 'direction',
        'account_sid', 'message_sid', 'from_str', 'to_str', 'uri',
        'error_message', 'error_code', 'api_version', 'from_user', 'to_user',
        'twilml_response_to__message_sid']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _twilio_outbound_message_fields})
    ]
    autocomplete_fields = ['message_template', 'from_user', 'to_user',
        'twilml_response_to']

_twilio_status_callback_fields = ['from_str', 'to_str', 'account_sid',
    'api_version', 'channel_to_address', 'channel_install_sid',
    'channel_status_message', 'channel_prefix', 'message_sid', 'message_status',
    'sms_sid', 'sms_status', 'error_code', 'event_type', 'message']
@admin.register(mod.TwilioStatusCallback)
class TwilioStatusCallbackAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _twilio_status_callback_fields
    list_editable = comadm.standard_list_editable + \
        _twilio_status_callback_fields
    list_filter = comadm.standard_list_filter + ['api_version',
        'channel_status_message', 'channel_prefix', 'message_status',
        'error_code', 'event_type']
    search_fields = comadm.standard_search_fields + ['from_str', 'to_str',
        'account_sid', 'api_version', 'channel_to_address',
        'channel_install_sid', 'channel_status_message', 'channel_prefix',
        'message_sid', 'message_status', 'sms_sid', 'sms_status', 'error_code',
        'event_type', 'message__body', 'log_entry__payload']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _twilio_status_callback_fields})
    ]
    autocomplete_fields = ['message']

_twilio_status_callback_log_entries_fields = ['payload', 'callback']
@admin.register(mod.TwilioStatusCallbackLogEntry)
class TwilioStatusCallbackLogEntryAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + \
        _twilio_status_callback_log_entries_fields
    list_editable = comadm.standard_list_editable + \
        _twilio_status_callback_log_entries_fields
    search_fields = comadm.standard_search_fields + ['payload']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _twilio_status_callback_log_entries_fields})
    ]
    autocomplete_fields = ['callback']

_twilio_inbound_message_request_fields = ['api_version',
    'message_sid', 'sms_sid', 'sms_message_sid', 'account_sid',
    'message_service_sid', 'from_str', 'to_str', 'body', 'num_media',
    'num_segment']
_twilio_inbound_message_geographic_fields = ['from_city', 'from_state',
    'from_zip', 'from_country', 'to_city', 'to_state', 'to_zip', 'to_country']
_twilio_inbound_message_whatsapp_fields = ['profile_name', 'wa_id', 'forwarded',
    'frequently_forwarded']
_twilio_inbound_message_whatsapp_location_fields = ['latitude', 'longitude',
    'address', 'label']
@admin.register(mod.TwilioInboundMessage)
class TwilioInboundMessage(comadm.StandardAdmin):
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
    search_fields = comadm.standard_search_fields + ['api_version',
        'message_sid', 'sms_sid', 'sms_message_sid', 'account_sid',
        'message_service_sid', 'from_str', 'to_str', 'body', 'from_city',
        'from_state', 'from_zip', 'from_country', 'to_city', 'to_state',
        'to_zip', 'to_country', 'profile_name', 'wa_id', 'address', 'label']

    # Details page settings
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

_twilio_inbound_message_media_fields = ['content_type', 'url', 'message']
@admin.register(mod.TwilioInboundMessageMedia)
class TwilioInboundMessageMediaAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + \
        _twilio_inbound_message_media_fields
    list_editable = comadm.standard_list_editable + \
        _twilio_inbound_message_media_fields
    search_fields = comadm.standard_search_fields + ['content_type',
        'url', 'message__body']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _twilio_inbound_message_media_fields})
    ]
    autocomplete_fields = ['message']

_twilio_inbound_message_log_entry = ['payload', 'message']
@admin.register(mod.TwilioInboundMessageLogEntry)
class TwilioInboundMessageLogEntryAdmin(comadm.StandardAdmin):
        # List page settings
    list_display = comadm.standard_list_display + \
        _twilio_inbound_message_log_entry
    list_editable = comadm.standard_list_editable + \
        _twilio_inbound_message_log_entry
    search_fields = comadm.standard_search_fields + \
        _twilio_inbound_message_log_entry

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _twilio_inbound_message_log_entry})
    ]
    autocomplete_fields = ['message']

_user_chat_context_fields = ['started', 'stopped', 'user', 'chat_context_type']
@admin.register(mod.UserChatContext)
class UserChatContextAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + \
        _user_chat_context_fields
    list_editable = comadm.standard_list_editable + \
        _user_chat_context_fields
    list_filter = comadm.standard_list_filter + ['started', 'stopped',
        'chat_context_type']
    search_fields = comadm.standard_search_fields + ['user__name']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _user_chat_context_fields})
    ]
    autocomplete_fields = ['user', 'chat_context_type']

@admin.register(mod.ChatContextType)
class ChatContextTypeAdmin(comadm.ChoiceAdmin):
    pass