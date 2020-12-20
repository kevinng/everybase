from django.contrib import admin
from . import models as mod
from files import models as fod
from communication import models as cod
from common import admin as comadm
from relationships import admin as reladm

# --- Start: Abstract configurations ---

# Expirable/Invalidable

_expirable_invalidable_fields = ['received', 'expired', 'invalidated',
    'invalidated_reason_md']
_expirable_invalidable_fieldsets = \
    [('Expirable and invalidable fields',
        {'fields': _expirable_invalidable_fields})]
_expirable_invalidable_filter = ['expired', 'invalidated']
_expirable_search_fields = ['invalidated_reason_md']

# Lead

_lead_fields = ['contact', 'company', 'category', 'display_name', 'base_uom',
    'details_md', 'contact_type', 'contact_type_details_md']
_lead_fieldsets = [
    ('Lead details', {'fields': _lead_fields})
]
_lead_filter = ['category', 'base_uom', 'contact_type', 'company']
_lead_autocomplete_fields = ['category', 'base_uom', 'contact', 'company',
    'contact_type']
_lead_search_fields = ['category', 'display_name', 'details_md', 'contact',
    'company', 'contact_type', 'contact_type_details_md']

# Quote

_quote_fields = ['details_md', 'incoterm', 'incoterm_country',
    'incoterm_location', 'currency', 'price', 'price_details_md',
    'deposit_percent', 'payterms_details_md', 'delivery_details_md']

# --- End: Abstract configurations ---

# --- Start: Inline ---

class DemandCommissionInlineAdmin(admin.TabularInline):
    model = mod.DemandCommission
    extra = 1
    autocomplete_fields = ['demand', 'quote', 'person', 'company']

class DemandQuoteInlineAdmin(admin.TabularInline):
    model = mod.DemandQuote
    extra = 1
    autocomplete_fields = ['incoterm', 'incoterm_country', 'status',
        'currency', 'deposit_paymodes', 'remainder_paymodes',
        'positive_origin_countries', 'negative_origin_countries']

class FileDemandInlineAdmin(admin.TabularInline):
    model = fod.FileDemand
    extra = 1
    autocomplete_fields = ['rtype', 'file']

class FileSupplyInlineAdmin(admin.TabularInline):
    model = fod.FileSupply
    extra = 1
    autocomplete_fields = ['rtype', 'file']

class IssueInlineAdmin(admin.TabularInline):
    model = cod.Issue
    extra = 1
    autocomplete_fields = ['tags', 'status', 'supply', 'demand', 'match',
        'supply_commission', 'demand_commission', 'supply_quote',
        'demand_quote']

class MatchInlineAdmin(admin.TabularInline):
    model = mod.Match
    extra = 1
    autocomplete_fields = ['supply_quote', 'demand_quote', 'status', 'method']

class ProductionCapacityInlineAdmin(admin.TabularInline):
    model = mod.ProductionCapability
    extra = 1

class SupplyCommissionInlineAdmin(admin.TabularInline):
    model = mod.SupplyCommission
    extra = 1
    autocomplete_fields = ['supply', 'quote', 'person', 'company']

class SupplyQuoteInlineAdmin(admin.TabularInline):
    model = mod.SupplyQuote
    extra = 1
    autocomplete_fields = ['incoterm', 'incoterm_country',
        'currency', 'deposit_paymodes', 'remainder_paymodes', 'status']

class TrenchInlineAdmin(admin.TabularInline):
    model = mod.Trench
    extra = 1
    autocomplete_fields = ['paymode', 'demand_quote', 'supply_quote']

class SupplyLinkInlineAdmin(admin.TabularInline):
    model = mod.SupplyLink
    extra = 1
    autocomplete_fields = ['rtype', 'supply', 'link']

class DemandLinkInlineAdmin(admin.TabularInline):
    model = mod.DemandLink
    extra = 1
    autocomplete_fields = ['rtype', 'demand', 'link']

# --- End: Inline ---

# --- Start: Relationships ---

_rel_list_display = comadm.standard_list_display + \
    ['details_md', 'rtype', 'link']

_rel_list_editable = comadm.standard_list_editable + \
    ['details_md', 'rtype', 'link']

_rel_list_search_fields = ['id', 'details_md', 'rtype', 'link']

_rel_fieldsets = lambda field: comadm.standard_fieldsets + [
    (None, {'fields': ['details_md', 'rtype', 'link', field]})]

_rel_autocomplete_fields = ['rtype', 'link']

@admin.register(
    mod.SupplyLinkType,
    mod.DemandLinkType)
class ChoiceAdmin(comadm.ChoiceAdmin):
    pass

@admin.register(mod.SupplyLink)
class SupplyLinkAdmin(reladm.RelationshipAdmin):
    # List page settings
    list_display = _rel_list_display + ['supply']
    list_editable = _rel_list_editable + ['supply']
    search_fields = _rel_list_search_fields + ['supply']

    # Details page settings
    fieldsets = _rel_fieldsets('supply')
    autocomplete_fields = _rel_autocomplete_fields + ['supply']

@admin.register(mod.DemandLink)
class DemandLinkAdmin(reladm.RelationshipAdmin):
    # List page settings
    list_display = _rel_list_display + ['demand']
    list_editable = _rel_list_editable + ['demand']
    search_fields = _rel_list_search_fields + ['demand']

    # Details page settings
    fieldsets = _rel_fieldsets('demand')
    autocomplete_fields = _rel_autocomplete_fields + ['demand']

# --- End: Relationships ---

# --- Start: Configurations ---

@admin.register(
    mod.ContactType,
    mod.Currency,
    mod.DemandQuoteStatus,
    mod.Incoterm,
    mod.MatchMethod,
    mod.MatchStatus,
    mod.PaymentMode,
    mod.SupplyQuoteStatus)
class ChoiceAdmin(comadm.ChoiceAdmin):
    pass

@admin.register(mod.LeadCategory)
class LeadCategoryAdmin(comadm.ChoiceAdmin):
    list_display = comadm.choice_list_display
    list_editable = comadm.choice_list_editable
    fieldsets = comadm.choice_fieldsets + \
        [('Model references', {'fields': ['parents']})]
    search_fields = comadm.choice_search_fields
    autocomplete_fields = ['parents']

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
class UnitOfMeasureAdmin(comadm.ChoiceAdmin):
    # List page settings
    list_display = comadm.choice_list_display + ['category']
    list_editable = comadm.choice_list_editable + ['category']
    list_filter = ['category']
    search_fields = comadm.choice_search_fields + \
        ['category__name', 'category__programmatic_key', 'details_md',
            'programmatic_details_md']

    # Details page settings
    fieldsets = comadm.choice_fieldsets + [(None, {'fields': ['category']})]
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
    list_per_page = 50
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
    list_display = comadm.standard_list_display + \
        _lead_fields + \
        _expirable_invalidable_fields # Display at the back
    list_editable = comadm.standard_list_editable + \
        _lead_fields + \
        _expirable_invalidable_fields # Display at the back
    list_per_page = 50
    list_filter = comadm.standard_list_filter + \
        _expirable_invalidable_filter + \
        _lead_filter
    search_fields = ['id'] + \
        _expirable_search_fields + \
        _lead_search_fields
    show_full_result_count = True

    # Details page settings
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + \
        _expirable_invalidable_fieldsets + \
        _lead_fieldsets
    autocomplete_fields = _lead_autocomplete_fields
    inlines = [SupplyQuoteInlineAdmin, SupplyCommissionInlineAdmin,
        FileSupplyInlineAdmin, SupplyLinkInlineAdmin]

@admin.register(mod.Demand)
class DemandAdmin(admin.ModelAdmin):
    search_fields = ['id']
    list_display = comadm.standard_list_display + \
        _expirable_invalidable_fields + \
        _lead_fields
    list_editable = comadm.standard_list_editable + \
        _expirable_invalidable_fields + \
        _lead_fields
    list_per_page = 50
    list_filter = comadm.standard_list_filter + \
        _expirable_invalidable_filter + \
        _lead_filter
    search_fields = ['id'] + \
        _expirable_search_fields + \
        _lead_search_fields
    show_full_result_count = True

    # Details page settings
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + \
        _expirable_invalidable_fieldsets + \
        _lead_fieldsets
    autocomplete_fields = _lead_autocomplete_fields
    inlines = [FileDemandInlineAdmin, DemandQuoteInlineAdmin,
        DemandCommissionInlineAdmin, DemandLinkInlineAdmin]

@admin.register(mod.DemandCommission)
class DemandCommissionAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + \
        ['demand', 'person', 'company']
    list_editable = comadm.standard_list_editable + \
        ['demand', 'person', 'company']
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['demand', 'person', 'company']
    search_fields = ['id', 'demand', 'person', 'company']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    fieldsets = comadm.standard_fieldsets + [
        (None, {'fields': ['quote', 'demand', 'person', 'company']})]
    autocomplete_fields = ['quote', 'demand', 'person', 'company']

_demand_quote_fields = ['demand', 'status', 'details_as_received_md',
    'negative_details_md']
@admin.register(mod.DemandQuote)
class DemandQuoteAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + \
        _demand_quote_fields + \
        _quote_fields
    list_editable = comadm.standard_list_editable + \
        _demand_quote_fields + \
        _quote_fields
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['status']
    search_fields = ['id', 'demand__display_name', 'demand__deetails_md',
        'details_as_received_md', 'negative_details_md']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + \
        _expirable_invalidable_fieldsets + \
        [('Details', {'fields': _demand_quote_fields + [
            'positive_origin_countries', 'negative_origin_countries'] + \
            _quote_fields})]
    autocomplete_fields = ['demand', 'status', 'positive_origin_countries',
        'negative_origin_countries', 'incoterm', 'incoterm_country',
        'currency']
    inlines = [DemandCommissionInlineAdmin, MatchInlineAdmin, TrenchInlineAdmin,
        IssueInlineAdmin]

@admin.register(mod.SupplyCommission)
class SupplyCommissionAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + \
        ['supply', 'person', 'company']
    list_editable = comadm.standard_list_editable + \
        ['supply', 'person', 'company']
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['supply', 'person', 'company']
    search_fields = ['id', 'supply', 'person', 'company']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    fieldsets = comadm.standard_fieldsets + \
        [(None, {'fields': ['quote', 'supply', 'person', 'company']})]
    autocomplete_fields = ['quote', 'supply', 'person', 'company']

_supply_quote_fields = ['supply', 'status', 'packing_details_md']
@admin.register(mod.SupplyQuote)
class SupplyQuoteAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + \
        _supply_quote_fields + \
        _quote_fields
    list_editable = comadm.standard_list_editable + \
        _supply_quote_fields + \
        _quote_fields
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['status', 'incoterm',
        'currency']
    search_fields = ['id', 'supply__display_name', 'supply__details_md',
        'packing_details_md', 'details_md', 'price_details_md',
        'payterms_details_md', 'delivery_details_md']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + \
        _expirable_invalidable_fieldsets + \
        [('Details', {'fields': _supply_quote_fields + _quote_fields})]
    autocomplete_fields = ['supply', 'status', 'incoterm', 'incoterm_country',
        'currency']
    inlines = [ProductionCapacityInlineAdmin, SupplyCommissionInlineAdmin,
        MatchInlineAdmin, TrenchInlineAdmin, IssueInlineAdmin]

@admin.register(mod.Match)
class MatchAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + \
        ['demand_quote', 'supply_quote', 'status', 'method', 'details_md']
    list_editable = comadm.standard_list_editable + \
        ['demand_quote', 'supply_quote', 'status', 'method', 'details_md']
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['status', 'method']
    search_fields = ['id', 'demand_quote', 'supply_quote', 'status', 'method',
        'details_md']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + \
        [('Match details', {'fields': ['demand_quote', 'supply_quote', 'status',
            'method', 'details_md']})]
    autocomplete_fields = ['demand_quote', 'supply_quote', 'status', 'method']
    inlines = [IssueInlineAdmin]

@admin.register(mod.ProductionCapability)
class ProductionCapabilityAdmin(admin.ModelAdmin):
    # List page settings
    list_display = comadm.standard_list_display + ['supply_quote', \
        'details_md', 'start', 'end', 'capacity_quantity', 'capacity_seconds']
    list_editable = comadm.standard_list_editable + ['supply_quote', \
        'details_md', 'start', 'end', 'capacity_quantity', 'capacity_seconds']
    list_per_page = 50
    list_filter = comadm.standard_list_filter + ['start', 'end']
    search_fields = ['id', 'supply_quote', 'details_md']
    ordering = comadm.standard_ordering
    show_full_result_count = True

    # Details page settings
    readonly_fields = comadm.standard_readonly_fields
    fieldsets = comadm.standard_fieldsets + \
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
    list_per_page = 50
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

# --- End: Configurations ----