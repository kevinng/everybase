from django.contrib import admin
from common.admin import (ChoiceAdmin, choice_fieldsets, choice_list_display,
    choice_list_editable, standard_list_display, standard_list_editable,
    standard_list_filter, standard_ordering, standard_fieldsets,
    standard_readonly_fields)

from . import models as mod

# --- Start: Abstract configurations ---

# Expirable/Invalidable

_expirable_invalidable_fields = ['expired', 'invalidated',
    'invalidated_reason_md']
_expirable_invalidable_fieldsets = \
    [(None, {'fields': _expirable_invalidable_fields})]
_expirable_invalidable_filter = ['expired', 'invalidated']
_expirable_search_fields = ['invalidated_reason_md']

# Lead

_lead_fields = ['category', 'display_name', 'base_uom', 'details_md',
    'contact', 'company', 'contact_type', 'contact_type_details_md']
_lead_fieldsets = [('Lead details', {'fields': _lead_fields})]
_lead_filter = ['category', 'base_uom', 'contact_type']
_lead_autocomplete_fields = ['category', 'base_uom', 'contact', 'company',
    'contact_type']
_lead_search_fields = ['category', 'display_name', 'details_md', 'contact',
    'company', 'contact_type', 'contact_type_details_md']

# --- End: Abstract configurations ---

@admin.register(
    mod.ContactType,
    mod.Currency,
    mod.DemandQuoteStatus,
    mod.Incoterm,
    mod.MatchMethod,
    mod.MatchStatus,
    mod.PaymentMode,
    mod.SupplyQuoteStatus)
class ChoiceAdmin(ChoiceAdmin):
    pass

@admin.register(mod.LeadCategory)
class LeadCategoryAdmin(ChoiceAdmin):
    list_display = choice_list_display + ['parent']
    list_editable = choice_list_editable + ['parent']
    fieldsets = choice_fieldsets + \
        [('Model references', {'fields': ['parent']})]
    autocomplete_fields = ['parent']

class UOMRelationshipChildInline(admin.StackedInline):
    model = mod.UOMRelationship
    fk_name = 'child'
    verbose_name = 'Parent UOM Relationship'
    verbose_name_plurals = 'Parent UOM Relationships'

class UOMRelationshipParentInline(admin.StackedInline):
    model = mod.UOMRelationship
    fk_name = 'parent'
    verbose_name = 'Child UOM Relationship'
    verbose_name_plurals = 'Child UOM Relationships'

@admin.register(mod.UnitOfMeasure)
class UnitOfMeasureAdmin(ChoiceAdmin):
    # List page settings
    list_display = choice_list_display + ['category']
    list_editable = choice_list_editable + ['category']
    list_filter = ['category']
    search_fields = ['id', 'category', 'parents']

    # Details page settings
    fieldsets = choice_fieldsets + [(None, {'fields': ['category']})]
    autocomplete_fields = ['category']
    inlines = [
        UOMRelationshipChildInline,
        UOMRelationshipParentInline
    ]

_uom_relationship_fields = ['child', 'parent', 'multiple', 'details_md']
@admin.register(mod.UOMRelationship)
class UOMRelationshipAdmin(admin.ModelAdmin):
    # List page settings
    list_display = ['id'] + _uom_relationship_fields
    list_editable = _uom_relationship_fields
    list_per_page = 1000
    list_filter = ['child', 'parent']
    search_fields = ['id', 'child', 'parent', 'details_md']
    ordering = ['id']
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = ['id']
    fieldsets = [
        (None, {'fields': ['id']}),
        (None, {'fields': _uom_relationship_fields})
    ]
    autocomplete_fields = ['child', 'parent']

@admin.register(mod.Supply)
class SupplyAdmin(admin.ModelAdmin):
    search_fields = ['id']
    list_display = standard_list_display + \
        _expirable_invalidable_fields + \
        _lead_fields
    list_editable = standard_list_editable + \
        _expirable_invalidable_fields + \
        _lead_fields
    list_per_page = 1000
    list_filter = standard_list_filter + \
        _expirable_invalidable_filter + \
        _lead_filter
    search_fields = ['id'] + \
        _expirable_search_fields + \
        _lead_search_fields
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = standard_readonly_fields
    fieldsets = standard_fieldsets + \
        _expirable_invalidable_fieldsets + \
        _lead_fieldsets
    autocomplete_fields = _lead_autocomplete_fields

@admin.register(mod.Demand)
class DemandAdmin(admin.ModelAdmin):
    search_fields = ['id']
    list_display = standard_list_display + \
        _expirable_invalidable_fields + \
        _lead_fields
    list_editable = standard_list_editable + \
        _expirable_invalidable_fields + \
        _lead_fields
    list_per_page = 1000
    list_filter = standard_list_filter + \
        _expirable_invalidable_filter + \
        _lead_filter
    search_fields = ['id'] + \
        _expirable_search_fields + \
        _lead_search_fields
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = standard_readonly_fields
    fieldsets = standard_fieldsets + \
        _expirable_invalidable_fieldsets + \
        _lead_fieldsets
    autocomplete_fields = _lead_autocomplete_fields

_demand_commission_fields = ['demand', 'person', 'company']
@admin.register(mod.DemandCommission)
class DemandCommissionAdmin(admin.ModelAdmin):
    # List page settings
    list_display = standard_list_display + _demand_commission_fields
    list_editable = standard_list_editable + _demand_commission_fields
    list_per_page = 1000
    list_filter = standard_list_filter + _demand_commission_fields
    search_fields = ['id'] + _demand_commission_fields
    ordering = standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = standard_readonly_fields
    fieldsets = standard_fieldsets + [
        (None, {'fields': ['quotes'] + _demand_commission_fields})]
    autocomplete_fields = ['quotes'] + _demand_commission_fields

_demand_quote_fields = ['demand', 'status', 'details_as_received_md',
    'negative_details_md']
@admin.register(mod.DemandQuote)
class DemandQuoteAdmin(admin.ModelAdmin):
    # List page settings
    list_display = standard_list_display + _demand_quote_fields
    list_editable = standard_list_editable + _demand_quote_fields
    list_per_page = 1000
    list_filter = standard_list_filter + ['demand', 'status']
    search_fields = ['id', 'positive_origin_countries',
        'negative_origin_countries'] + _demand_quote_fields
    ordering = standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = standard_readonly_fields
    fieldsets = standard_fieldsets + [
        (None, {'fields': ['positive_origin_countries',
            'negative_origin_countries'] + _demand_quote_fields})
    ]
    autocomplete_fields = ['demand', 'status', 'positive_origin_countries',
        'negative_origin_countries']

_supply_commission_fields = ['supply', 'person', 'company']
@admin.register(mod.SupplyCommission)
class SupplyCommissionAdmin(admin.ModelAdmin):
    # List page settings
    list_display = standard_list_display + _supply_commission_fields
    list_editable = standard_list_editable + _supply_commission_fields
    list_per_page = 1000
    list_filter = standard_list_filter + _supply_commission_fields
    search_fields = ['id'] + _supply_commission_fields
    ordering = standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = standard_readonly_fields
    fieldsets = standard_fieldsets + \
        [(None, {'fields': ['quotes'] + _supply_commission_fields})]
    autocomplete_fields = ['quotes'] + _supply_commission_fields

_supply_quote_fields = ['supply', 'status', 'packing_details_md']
@admin.register(mod.SupplyQuote)
class SupplyQuoteAdmin(admin.ModelAdmin):
    # List page settings
    list_display = standard_list_display + _supply_quote_fields
    list_editable = standard_list_editable + _supply_quote_fields
    list_per_page = 1000
    list_filter = standard_list_filter + ['status']
    search_fields = ['id'] + _supply_quote_fields
    ordering = standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = standard_readonly_fields
    fieldsets = standard_fieldsets + \
        [('Details', {'fields': _supply_quote_fields + ['downstreams']})]
    autocomplete_fields = ['supply', 'status', 'downstreams']

_match_details = ['demand_quote', 'supply_quote', 'status', 'method',
    'details_md']
@admin.register(mod.Match)
class MatchAdmin(admin.ModelAdmin):
    # List page settings
    list_display = standard_list_display + _match_details
    list_editable = standard_list_editable + _match_details
    list_per_page = 1000
    list_filter = standard_list_filter + ['status', 'method']
    search_fields = ['id'] + _match_details
    ordering = standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = standard_readonly_fields
    fieldsets = standard_fieldsets + \
        [('Match details', {'fields': _match_details})]
    autocomplete_fields = ['demand_quote', 'supply_quote', 'status', 'method']

_production_capability_fields = ['supply_quote', 'details_md', 'start', 'end',
    'capacity_quantity', 'capacity_seconds']
@admin.register(mod.ProductionCapability)
class ProductionCapabilityAdmin(admin.ModelAdmin):
    # List page settings
    list_display = standard_list_display + _production_capability_fields
    list_editable = standard_list_editable + _production_capability_fields
    list_per_page = 1000
    list_filter = standard_list_filter + ['start', 'end']
    search_fields = ['id', 'supply_quote', 'details_md']
    ordering = standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = standard_readonly_fields
    fieldsets = standard_fieldsets + \
        [(None, {'fields': _production_capability_fields})]
    autocomplete_fields = ['supply_quote']

_trench_fields = ['supply_quote', 'demand_quote', 'quantity',
    'after_deposit_seconds', 'paymode', 'payment_before_release', 'details_md']
@admin.register(mod.Trench)
class TrenchAdmin(admin.ModelAdmin):
    # List page settings
    list_display = ['id'] + _trench_fields
    list_editable = _trench_fields
    list_per_page = 1000
    list_filter = ['paymode', 'payment_before_release']
    search_fields = ['id', 'supply_quote', 'demand_quote', 'details_md']
    ordering = ['-id']
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    fieldsets = [(None, {'fields': _trench_fields})]
    autocomplete_fields = ['supply_quote', 'demand_quote', 'paymode']