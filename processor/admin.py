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

_base_truth_fields = ['message_group', 'method', 'text_output',
    'integer_output', 'float_output']
@admin.register(mod.BaseTruth)
class BaseTruthAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + _base_truth_fields
    list_editable = comadm.standard_list_editable + _base_truth_fields
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['method']
    search_fields = comadm.standard_search_fields + ['message_group__body',
        'method__name', 'method__description', 'text_output',
        'integer_output', 'float_output']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + [
        ('Details', {'fields': _base_truth_fields})
    ]
    autocomplete_fields = ['message_group', 'method']