from django.contrib import admin
from .models import (Incoterm, Currency, PaymentMode, ContactType, LeadCategory,
    MatchMethod, MatchStatus, SupplyQuoteStatus, DemandQuoteStatus,
    UnitOfMeasure, UOMRelationship, Supply, Demand, SupplyQuote, DemandQuote,
    ProductionCapability, Trench, Match, SupplyCommission, DemandCommission)
from common.admin import (ChoiceAdmin, choice_fieldsets, choice_list_display,
    choice_list_editable, standard_list_display, standard_list_editable,
    standard_list_filter, standard_ordering, standard_fieldsets,
    standard_readonly_fields)

# --- Start: Abstract configurations ---

# Expirable/Invalidable

expirable_invalidable_list_display = ['expired', 'invalidated',
    'invalidated_reason_md']

expirable_invalidable_list_editable = ['expired', 'invalidated',
    'invalidated_reason_md']

expirable_invalidable_fieldsets = [
    ('Expirable/Invalidable details', {'fields': ['expired', 'invalidated',
        'invalidated_reason_md']})
]

expirable_invalidable_filter = ['expired', 'invalidated']

expirable_search_fields = ['invalidated_reason_md']

# Lead

lead_list_display = ['category', 'display_name', 'base_uom', 'details_md',
    'contact', 'company', 'contact_type', 'contact_type_details_md']

lead_list_editable = ['category', 'display_name', 'base_uom', 'details_md',
    'contact', 'company', 'contact_type', 'contact_type_details_md']

lead_fieldsets = [
    ('Lead details', {'fields': ['category', 'display_name', 'base_uom',
        'details_md', 'files', 'contact', 'company', 'contact_type',
        'contact_type_details_md']})
]

lead_filter = ['category', 'base_uom', 'contact_type']

lead_autocomplete_fields = ['category', 'base_uom', 'files', 'contact',
    'company', 'contact_type']

lead_search_fields = ['category', 'display_name', 'details_md', 'contact',
    'company', 'contact_type', 'contact_type_details_md']

# --- End: Abstract configurations ---

@admin.register(ContactType, Currency, DemandQuoteStatus, Incoterm,
    MatchMethod, MatchStatus, PaymentMode, SupplyQuoteStatus)
class ChoiceAdmin(ChoiceAdmin):
    pass

@admin.register(LeadCategory)
class LeadCategoryAdmin(ChoiceAdmin):
    list_display = choice_list_display + ['parent']
    list_editable = choice_list_editable + ['parent']
    fieldsets = choice_fieldsets + [
        ('Model references', {'fields': ['parent']})
    ]
    autocomplete_fields = ['parent']

class UOMRelationshipChildInline(admin.StackedInline):
    model = UOMRelationship
    fk_name = 'child'
    verbose_name = 'Parent UOM Relationship'
    verbose_name_plurals = 'Parent UOM Relationships'

class UOMRelationshipParentInline(admin.StackedInline):
    model = UOMRelationship
    fk_name = 'parent'
    verbose_name = 'Child UOM Relationship'
    verbose_name_plurals = 'Child UOM Relationships'

@admin.register(UnitOfMeasure)
class UnitOfMeasureAdmin(ChoiceAdmin):
    # List page settings
    list_display = choice_list_display + ['category']
    list_editable = choice_list_editable + ['category']
    list_filter = ['category']
    search_fields = ['id', 'category', 'parents']

    # Details page settings
    fieldsets = choice_fieldsets + [
        ('Model references', {'fields': ['category']})]
    autocomplete_fields = ['category']
    inlines = [
        UOMRelationshipChildInline,
        UOMRelationshipParentInline
    ]

@admin.register(UOMRelationship)
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
        ('Details', {'fields': ['child', 'parent', 'multiple',
            'details_md']})
    ]
    autocomplete_fields = ['child', 'parent']

@admin.register(Supply)
class SupplyAdmin(admin.ModelAdmin):
    search_fields = ['id']
    list_display = standard_list_display + expirable_invalidable_list_display \
        + lead_list_display
    list_editable = standard_list_editable + \
        expirable_invalidable_list_editable + lead_list_editable
    list_per_page = 1000
    list_filter = standard_list_filter + expirable_invalidable_filter + \
        lead_filter
    search_fields = ['id'] + expirable_search_fields + lead_search_fields
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = standard_readonly_fields
    fieldsets = standard_fieldsets + expirable_invalidable_fieldsets + \
        lead_fieldsets
    autocomplete_fields = lead_autocomplete_fields

@admin.register(Demand)
class DemandAdmin(admin.ModelAdmin):
    search_fields = ['id']
    list_display = standard_list_display + expirable_invalidable_list_display \
        + lead_list_display
    list_editable = standard_list_editable + \
        expirable_invalidable_list_editable + lead_list_editable
    list_per_page = 1000
    list_filter = standard_list_filter + expirable_invalidable_filter + \
        lead_filter
    search_fields = ['id'] + expirable_search_fields + lead_search_fields
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = standard_readonly_fields
    fieldsets = standard_fieldsets + expirable_invalidable_fieldsets + \
        lead_fieldsets
    autocomplete_fields = lead_autocomplete_fields

@admin.register(DemandCommission)
class DemandCommissionAdmin(admin.ModelAdmin):
    # List page settings
    list_display = standard_list_display + ['demand', 'person', 'company']
    list_editable = standard_list_editable + ['demand', 'person', 'company']
    list_per_page = 1000
    list_filter = standard_list_filter + ['demand', 'person', 'company']
    search_fields = ['id', 'demand', 'person', 'company']
    ordering = standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = standard_readonly_fields
    fieldsets = standard_fieldsets + [
        ('Model references', {'fields': ['quotes', 'demand', 'person',
            'company']})
    ]
    autocomplete_fields = ['quotes', 'demand', 'person', 'company']

@admin.register(DemandQuote)
class DemandQuoteAdmin(admin.ModelAdmin):
    # List page settings
    list_display = standard_list_display + ['demand', 'status',
        'details_as_received_md', 'negative_details_md']
    list_editable = standard_list_editable + ['demand', 'status',
        'details_as_received_md', 'negative_details_md']
    list_per_page = 1000
    list_filter = standard_list_filter + ['demand', 'status']
    search_fields = ['id', 'demand', 'status', 'details_as_received_md',
        'negative_details_md', 'positive_origin_countries',
        'negative_origin_countries']
    ordering = standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = standard_readonly_fields
    fieldsets = standard_fieldsets + [
        ('Details', {'fields': ['demand', 'status', 'details_as_received_md',
            'positive_origin_countries', 'negative_origin_countries',
            'negative_details_md']})
    ]
    autocomplete_fields = ['demand', 'status', 'positive_origin_countries',
        'negative_origin_countries']

@admin.register(SupplyCommission)
class SupplyCommissionAdmin(admin.ModelAdmin):
    # List page settings
    list_display = standard_list_display + ['supply', 'person', 'company']
    list_editable = standard_list_editable + ['supply', 'person', 'company']
    list_per_page = 1000
    list_filter = standard_list_filter + ['supply', 'person', 'company']
    search_fields = ['id', 'supply', 'person', 'company']
    ordering = standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = standard_readonly_fields
    fieldsets = standard_fieldsets + [
        ('Model references', {'fields': ['quotes', 'supply', 'person',
            'company']})
    ]
    autocomplete_fields = ['quotes', 'supply', 'person', 'company']

@admin.register(SupplyQuote)
class SupplyQuoteAdmin(admin.ModelAdmin):
    # List page settings
    list_display = standard_list_display + ['supply', 'status',
        'packing_details_md']
    list_editable = standard_list_editable + ['supply', 'status',
        'packing_details_md']
    list_per_page = 1000
    list_filter = standard_list_filter + ['status']
    search_fields = ['id', 'supply', 'status', 'packing_details_md']
    ordering = standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = standard_readonly_fields
    fieldsets = standard_fieldsets + [
        ('Details', {'fields': ['supply', 'status', 'packing_details_md',
            'downstreams']})
    ]
    autocomplete_fields = ['supply', 'status', 'downstreams']

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    # List page settings
    list_display = standard_list_display + ['demand_quote', 'supply_quote',
        'status', 'method', 'details_md']
    list_editable = standard_list_editable + ['demand_quote', 'supply_quote',
        'status', 'method', 'details_md']
    list_per_page = 1000
    list_filter = standard_list_filter + ['status', 'method']
    search_fields = ['id', 'demand_quote', 'supply_quote', 'method',
        'details_md']
    ordering = standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = standard_readonly_fields
    fieldsets = standard_fieldsets + [
        ('Match details', {'fields': ['demand_quote', 'supply_quote', 'status',
            'method', 'details_md']})
    ]
    autocomplete_fields = ['demand_quote', 'supply_quote', 'status', 'method']

@admin.register(ProductionCapability)
class ProductionCapabilityAdmin(admin.ModelAdmin):
    # List page settings
    list_display = standard_list_display + ['supply_quote', 'details_md',
        'start', 'end', 'capacity_quantity', 'capacity_seconds']
    list_editable = standard_list_editable + ['supply_quote', 'details_md',
        'start', 'end', 'capacity_quantity', 'capacity_seconds']
    list_per_page = 1000
    list_filter = standard_list_filter + ['start', 'end']
    search_fields = ['id', 'supply_quote', 'details_md']
    ordering = standard_ordering
    show_full_result_count = True

    # Details page settings
    save_on_top = True
    readonly_fields = standard_readonly_fields
    fieldsets = standard_fieldsets + [
        ('Details', {'fields': ['supply_quote', 'details_md']}),
        ('Period', {'fields': ['start', 'end']}),
        ('Capacity', {'fields': ['capacity_quantity', 'capacity_seconds']})
    ]
    autocomplete_fields = ['supply_quote']

@admin.register(Trench)
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
    fieldsets = [
        ('Quote', {
            'fields': ['supply_quote', 'demand_quote'],
            'description': 'One of these quote must be set'}),
        ('Details', {
            'fields': ['quantity', 'after_deposit_seconds', 'paymode',
                'payment_before_release', 'details_md']})
    ]
    autocomplete_fields = ['supply_quote', 'demand_quote', 'paymode']