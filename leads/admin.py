from django.contrib import admin
from .models import (Incoterm, Currency, PaymentMode, ContactType, LeadCategory,
    MatchMethod, MatchStatus, SupplyQuoteStatus, DemandQuoteStatus,
    UnitOfMeasure, UOMRelationship, Supply, Demand, SupplyQuote, DemandQuote,
    ProductionCapability, Trench, Match, SupplyCommission, DemandCommission)
from common.admin import (ChoiceAdmin, choice_fieldsets, choice_list_display,
    choice_list_editable, standard_list_display, standard_list_editable,
    standard_list_filter, standard_ordering, standard_fieldsets,
    standard_readonly_fields)

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

class UnitOfMeasureAdmin(ChoiceAdmin):
    fieldsets = [
        (None, {'fields': ['id', 'name', 'details_md', 'category']}),
        ('Developer', {'fields': ['programmatic_key',
            'programmatic_details_md']})
    ]
    inlines = [
        UOMRelationshipChildInline,
        UOMRelationshipParentInline
    ]

class SupplyAdmin(admin.ModelAdmin):
    search_fields = ['id']

class DemandAdmin(admin.ModelAdmin):
    search_fields = ['id']

class SupplyQuoteAdmin(admin.ModelAdmin):
    search_fields = ['id']

class MatchAdmin(admin.ModelAdmin):
    search_fields = ['id']

class SupplyCommissionAdmin(admin.ModelAdmin):
    search_fields = ['id']



admin.site.register(UnitOfMeasure, UnitOfMeasureAdmin)
admin.site.register(UOMRelationship)
admin.site.register(Supply, SupplyAdmin)
admin.site.register(Demand, DemandAdmin)
admin.site.register(SupplyQuote, SupplyQuoteAdmin)
admin.site.register(ProductionCapability)
admin.site.register(Trench)
admin.site.register(Match, MatchAdmin)
admin.site.register(SupplyCommission, SupplyCommissionAdmin)


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





# class ZeroBounceResultAdmin(admin.ModelAdmin):
#     # List page settings
#     list_display = standard_list_display + ['email_address', 'status',
#         'sub_status', 'account', 'domain', 'first_name', 'last_name', 'gender',
#         'free_email', 'mx_found', 'mx_record', 'smtp_provider', 'did_you_mean']
#     list_editable = standard_list_editable + ['email_address', 'status',
#         'sub_status', 'account', 'domain', 'first_name', 'last_name', 'gender',
#         'free_email', 'mx_found', 'mx_record', 'smtp_provider', 'did_you_mean']
#     
#     list_filter = standard_list_filter + ['status', 'sub_status', 'gender',
#         'free_email', 'mx_found']
#     search_fields = ['id', 'email_address', 'status', 'sub_status', 'account',
#         'domain', 'first_name', 'last_name', 'gender', 'free_email', 'mx_found',
#         'mx_record', 'smtp_provider', 'did_you_mean']
#     ordering = ['email_address']
#     show_full_result_count = True
    
#     # Details page settings

#     fieldsets = standard_fieldsets + [
#         ('Result details', {
#             'fields': ['email_address', 'status',
#             'sub_status', 'account', 'domain', 'first_name', 'last_name',
#             'gender', 'free_email', 'mx_found', 'mx_record', 'smtp_provider',
#             'did_you_mean']
#         }),
#         ('Model references', {
#             'fields': ['email']
#         })
#     ]
#     autocomplete_fields = ['email']