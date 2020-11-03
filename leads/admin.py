from django.contrib import admin
from . import models as mod
from common import admin as commod

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
class ChoiceAdmin(commod.ChoiceAdmin):
    pass

@admin.register(mod.LeadCategory)
class LeadCategoryAdmin(commod.ChoiceAdmin):
    list_display = commod.choice_list_display + ['parent']
    list_editable = commod.choice_list_editable + ['parent']
    fieldsets = commod.choice_fieldsets + \
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
class UnitOfMeasureAdmin(commod.ChoiceAdmin):
    # List page settings
    list_display = commod.choice_list_display + ['category']
    list_editable = commod.choice_list_editable + ['category']
    list_filter = ['category']
    search_fields = ['id', 'category', 'parents']

    # Details page settings
    fieldsets = commod.choice_fieldsets + [(None, {'fields': ['category']})]
    autocomplete_fields = ['category']
    inlines = [
        UOMRelationshipChildInline,
        UOMRelationshipParentInline
    ]

@admin.register(mod.UOMRelationship)
class UOMRelationshipAdmin(admin.ModelAdmin):
    # List page settings
    list_display = ['id', 'child', 'parent', 'multiple', 'details_md']
    list_editable = ['child', 'parent', 'multiple', 'details_md']
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
        (None, {'fields': ['child', 'parent', 'multiple', 'details_md']})
    ]
    autocomplete_fields = ['child', 'parent']

@admin.register(mod.Supply)
class SupplyAdmin(admin.ModelAdmin):
    search_fields = ['id']
    list_display = commod.standard_list_display + \
        _expirable_invalidable_fields + \
        _lead_fields
    list_editable = commod.standard_list_editable + \
        _expirable_invalidable_fields + \
        _lead_fields
    list_per_page = 1000
    list_filter = commod.standard_list_filter + \
        _expirable_invalidable_filter + \
        _lead_filter
    search_fields = ['id'] + \
        _expirable_search_fields + \
        _lead_search_fields
    show_full_result_count = True

    # Details page settings
    fieldsets = commod.standard_fieldsets + \
        _expirable_invalidable_fieldsets + \
        _lead_fieldsets
    autocomplete_fields = _lead_autocomplete_fields

@admin.register(mod.Demand)
class DemandAdmin(admin.ModelAdmin):
    search_fields = ['id']
    list_display = commod.standard_list_display + \
        _expirable_invalidable_fields + \
        _lead_fields
    list_editable = commod.standard_list_editable + \
        _expirable_invalidable_fields + \
        _lead_fields
    list_per_page = 1000
    list_filter = commod.standard_list_filter + \
        _expirable_invalidable_filter + \
        _lead_filter
    search_fields = ['id'] + \
        _expirable_search_fields + \
        _lead_search_fields
    show_full_result_count = True

    # Details page settings
    fieldsets = commod.standard_fieldsets + \
        _expirable_invalidable_fieldsets + \
        _lead_fieldsets
    autocomplete_fields = _lead_autocomplete_fields

@admin.register(mod.DemandCommission)
class DemandCommissionAdmin(admin.ModelAdmin):
    # List page settings
    list_display = commod.standard_list_display + \
        ['demand', 'person', 'company']
    list_editable = commod.standard_list_editable + \
        ['demand', 'person', 'company']
    list_per_page = 1000
    list_filter = commod.standard_list_filter + ['demand', 'person', 'company']
    search_fields = ['id', 'demand', 'person', 'company']
    ordering = commod.standard_ordering
    show_full_result_count = True

    # Details page settings
    fieldsets = commod.standard_fieldsets + [
        (None, {'fields': ['quotes', 'demand', 'person', 'company']})]
    autocomplete_fields = ['quotes', 'demand', 'person', 'company']

@admin.register(mod.DemandQuote)
class DemandQuoteAdmin(admin.ModelAdmin):
    # List page settings
    list_display = commod.standard_list_display + ['demand', 'status',
        'details_as_received_md', 'negative_details_md']
    list_editable = commod.standard_list_editable + ['demand', 'status',
        'details_as_received_md', 'negative_details_md']
    list_per_page = 1000
    list_filter = commod.standard_list_filter + ['demand', 'status']
    search_fields = ['id', 'positive_origin_countries',
        'negative_origin_countries'] + ['demand', 'status',
        'details_as_received_md', 'negative_details_md']
    ordering = commod.standard_ordering
    show_full_result_count = True

    # Details page settings
    fieldsets = commod.standard_fieldsets + [
        (None, {'fields': ['positive_origin_countries',
            'negative_origin_countries', 'demand', 'status',
            'details_as_received_md', 'negative_details_md']})
    ]
    autocomplete_fields = ['demand', 'status', 'positive_origin_countries',
        'negative_origin_countries']

@admin.register(mod.SupplyCommission)
class SupplyCommissionAdmin(admin.ModelAdmin):
    # List page settings
    list_display = commod.standard_list_display + \
        ['supply', 'person', 'company']
    list_editable = commod.standard_list_editable + \
        ['supply', 'person', 'company']
    list_per_page = 1000
    list_filter = commod.standard_list_filter + ['supply', 'person', 'company']
    search_fields = ['id', 'supply', 'person', 'company']
    ordering = commod.standard_ordering
    show_full_result_count = True

    # Details page settings
    fieldsets = commod.standard_fieldsets + \
        [(None, {'fields': ['quotes', 'supply', 'person', 'company']})]
    autocomplete_fields = ['quotes', 'supply', 'person', 'company']

@admin.register(mod.SupplyQuote)
class SupplyQuoteAdmin(admin.ModelAdmin):
    # List page settings
    list_display = commod.standard_list_display + ['supply', 'status',
        'packing_details_md']
    list_editable = commod.standard_list_editable + ['supply', 'status',
        'packing_details_md']
    list_per_page = 1000
    list_filter = commod.standard_list_filter + ['status']
    search_fields = ['id'] + ['supply', 'status', 'packing_details_md']
    ordering = commod.standard_ordering
    show_full_result_count = True

    # Details page settings
    fieldsets = commod.standard_fieldsets + \
        [('Details', {'fields': ['supply', 'status', 'packing_details_md',
            'downstreams']})]
    autocomplete_fields = ['supply', 'status', 'downstreams']

@admin.register(mod.Match)
class MatchAdmin(admin.ModelAdmin):
    # List page settings
    list_display = commod.standard_list_display + \
        ['demand_quote', 'supply_quote', 'status', 'method', 'details_md']
    list_editable = commod.standard_list_editable + \
        ['demand_quote', 'supply_quote', 'status', 'method', 'details_md']
    list_per_page = 1000
    list_filter = commod.standard_list_filter + ['status', 'method']
    search_fields = ['id', 'demand_quote', 'supply_quote', 'status', 'method',
        'details_md']
    ordering = commod.standard_ordering
    show_full_result_count = True

    # Details page settings
    fieldsets = commod.standard_fieldsets + \
        [('Match details', {'fields': ['demand_quote', 'supply_quote', 'status',
            'method', 'details_md']})]
    autocomplete_fields = ['demand_quote', 'supply_quote', 'status', 'method']

@admin.register(mod.ProductionCapability)
class ProductionCapabilityAdmin(admin.ModelAdmin):
    # List page settings
    list_display = commod.standard_list_display + ['supply_quote', \
        'details_md', 'start', 'end', 'capacity_quantity', 'capacity_seconds']
    list_editable = commod.standard_list_editable + ['supply_quote', \
        'details_md', 'start', 'end', 'capacity_quantity', 'capacity_seconds']
    list_per_page = 1000
    list_filter = commod.standard_list_filter + ['start', 'end']
    search_fields = ['id', 'supply_quote', 'details_md']
    ordering = commod.standard_ordering
    show_full_result_count = True

    # Details page settings
    fieldsets = commod.standard_fieldsets + \
        [(None, {'fields': ['supply_quote', 'details_md', 'start', 'end',
            'capacity_quantity', 'capacity_seconds']})]
    autocomplete_fields = ['supply_quote']

@admin.register(mod.Trench)
class TrenchAdmin(admin.ModelAdmin):
    # List page settings
    list_display = ['id', 'supply_quote', 'demand_quote', 'quantity',
        'after_deposit_seconds', 'paymode', 'payment_before_release',
        'details_md']
    list_editable = ['supply_quote', 'demand_quote', 'quantity',
        'after_deposit_seconds', 'paymode', 'payment_before_release',
        'details_md']
    list_per_page = 1000
    list_filter = ['paymode', 'payment_before_release']
    search_fields = ['id', 'supply_quote', 'demand_quote', 'details_md']
    ordering = ['-id']
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    fieldsets = [(None, {'fields': ['supply_quote', 'demand_quote', 'quantity',
        'after_deposit_seconds', 'paymode', 'payment_before_release',
        'details_md']})]
    autocomplete_fields = ['supply_quote', 'demand_quote', 'paymode']