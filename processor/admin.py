from django.contrib import admin

from . import models as mod
from common import admin as comadm

# ----- Start: Inlines -----

class MessageBodyMetaDataInlineAdmin(admin.TabularInline):
    model = mod.MessageBodyMetaData
    extra = 1
    autocomplete_fields = ['twilio_inbound_message', 'test_message']

class MessageBodyMetaDataEntityInlineAdmin(admin.TabularInline):
    model = mod.MessageBodyMetaDataEntity
    extra = 1
    autocomplete_fields = ['meta_data']

# ----- End: Inlines -----

_test_message_fields = ['body']
@admin.register(mod.TestMessage)
class TestMessageAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _test_message_fields
    list_editable = comadm.standard_list_editable + _test_message_fields
    search_fields = comadm.standard_search_fields + _test_message_fields
    list_per_page = 500

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _test_message_fields})
    ]
    inlines = [MessageBodyMetaDataInlineAdmin]

_message_body_meta_data_fields = ['group', 'ran', 'is_base_truth',
    'is_enabled', 'version', 'body_copy', 'twilio_inbound_message',
    'test_message']
@admin.register(mod.MessageBodyMetaData)
class MessageBodyMetaDataAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + \
        _message_body_meta_data_fields
    list_editable = comadm.standard_list_editable + \
        _message_body_meta_data_fields
    search_fields = comadm.standard_search_fields + \
        _message_body_meta_data_fields
    list_per_page = 500

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _message_body_meta_data_fields})
    ]
    inlines = [MessageBodyMetaDataEntityInlineAdmin]

_message_body_meta_data_entity_fields = ['start_position', 'end_position',
    'boolean_value', 'numeric_value', 'string_value', 'substring',
    'programmatic_key_1', 'programmatic_key_2']
@admin.register(mod.MessageBodyMetaDataEntity)
class MessageBodyMetaDataEntityAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + \
        _message_body_meta_data_entity_fields
    list_editable = comadm.standard_list_editable + \
        _message_body_meta_data_entity_fields
    search_fields = comadm.standard_search_fields + \
        _message_body_meta_data_entity_fields
    list_per_page = 500

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _message_body_meta_data_entity_fields})
    ]

_matching_keyword_fields = ['keyword', 'edit_distance_tolerance', 'currency',
    'excluded_price', 'location', 'incoterm_availability', 'application',
    'company', 'product_type', 'product', 'product_specification_type',
    'unit_of_measure']
@admin.register(mod.MatchingKeyword)
class MatchingKeywordAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _matching_keyword_fields
    list_editable = comadm.standard_list_editable + _matching_keyword_fields
    search_fields = comadm.standard_search_fields + _matching_keyword_fields

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _matching_keyword_fields})
    ]
    autocomplete_fields = ['currency', 'excluded_price', 'location',
        'incoterm_availability', 'application', 'company', 'product_type',
        'product', 'product_specification_type', 'unit_of_measure']