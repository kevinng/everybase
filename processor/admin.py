from django.contrib import admin

from . import models as mod
from common import admin as comadm

_message_fields = ['body']
@admin.register(mod.TestMessageGroup)
class TestMessageGroupAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _message_fields
    list_editable = comadm.standard_list_editable + _message_fields
    search_fields = comadm.standard_search_fields + _message_fields

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _message_fields})
    ]

_base_truth_fields = ['message_group', 'text_output', 'method',
    'integer_output', 'float_output']
@admin.register(mod.BaseTruth)
class BaseTruthAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _base_truth_fields
    list_editable = comadm.standard_list_editable + _base_truth_fields
    list_filter = comadm.standard_list_filter + ['method']
    search_fields = comadm.standard_search_fields + ['message_group__body',
        'text_output', 'integer_output', 'float_output']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _base_truth_fields})
    ]
    autocomplete_fields = ['message_group', 'method']

_inbound_message_group_fields = ['is_disabled', 'grouped', 'initial_body']
@admin.register(mod.InboundMessageGroup)
class InboundMessageGroupAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _inbound_message_group_fields
    list_editable = comadm.standard_list_editable + \
        _inbound_message_group_fields
    list_filter = comadm.standard_list_filter + ['grouped']
    search_fields = comadm.standard_search_fields + ['initial_body']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _inbound_message_group_fields + \
            ['twilio_inbound_messages']})
    ]
    autocomplete_fields = ['twilio_inbound_messages']

_grouping_method_fields = ['applied', 'order', 'inbound_message_group',
    'method']
@admin.register(mod.GroupingMethod)
class GroupingMethodAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _grouping_method_fields
    list_editable = comadm.standard_list_editable + \
        _grouping_method_fields
    list_filter = comadm.standard_list_filter + ['applied', 'method']
    search_fields = comadm.standard_search_fields + [
        'inbound_message_group__initial_body', 'method__title']

    # Details page settings
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
class MethodAdmin(comadm.StandardChoiceAdmin):
    # List page settings
    list_display = comadm.standard_choice_list_display + _method_fields
    list_editable = comadm.standard_choice_list_editable + _method_fields
    list_filter = comadm.standard_choice_list_filter + ['tags']
    search_fields = comadm.standard_choice_search_fields + ['title', 'version']

    # Details page settings
    readonly_fields = comadm.standard_choice_readonly_fields
    fieldsets = comadm.standard_choice_fieldsets + [
        ('Details', {'fields': _method_fields + ['tags']})
    ]
    autocomplete_fields = ['tags']

@admin.register(mod.MethodTag)
class MethodTagAdmin(comadm.StandardChoiceAdmin):
    pass

_inbound_message_group_relationship_fields = ['associated', 'group']
_inbound_message_group_relationship_m2m_fields = ['tags', 'supplies', 'demands',
    'supply_quotes', 'demand_quotes']
@admin.register(mod.InboundMessageGroupRelationship)
class InboundMessageGroupRelationshipAdmin(comadm.StandardAdmin):
    # List page settings
    list_display = comadm.standard_list_display + \
        _inbound_message_group_relationship_fields
    list_editable = comadm.standard_list_editable + \
        _inbound_message_group_relationship_fields
    list_filter = comadm.standard_list_filter + \
        _inbound_message_group_relationship_fields + \
        _inbound_message_group_relationship_m2m_fields
    search_fields = comadm.standard_search_fields + ['group__initial_body']

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _inbound_message_group_relationship_fields +\
            _inbound_message_group_relationship_m2m_fields})
    ]
    autocomplete_fields = _inbound_message_group_relationship_m2m_fields

@admin.register(mod.InboundMessageGroupRelationshipTag)
class InboundMessageGroupRelationshipTagAdmin(comadm.StandardChoiceAdmin):
    pass

_test_run_type_fields = ['setting']
@admin.register(mod.TestRunType)
class TestRunTypeAdmin(comadm.StandardChoiceAdmin):
    # List page settings
    list_display = comadm.standard_choice_list_display + _test_run_type_fields
    list_editable = comadm.standard_choice_list_editable + _test_run_type_fields
    list_filter = comadm.standard_choice_list_filter + ['setting']

    # Details page settings
    fieldsets = comadm.standard_choice_fieldsets + [
        ('Details', {'fields': _test_run_type_fields + ['methods']})
    ]
    autocomplete_fields = ['methods']