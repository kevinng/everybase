from django.contrib import admin
from .models import (Incoterm, Currency, PaymentMode, ContactType, LeadCategory,
    MatchMethod, MatchStatus, SupplyQuoteStatus, DemandQuoteStatus,
    UnitOfMeasure, UOMRelationship, Supply, Demand, SupplyQuote, DemandQuote,
    ProductionCapability, Trench, Match, SupplyCommission, DemandCommission)
from common.admin import (ChoiceAdmin, choice_fieldsets, choice_list_display,
    choice_list_editable)

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
        ('Developer', {
                'fields': [
                    'programmatic_key', 
                    'programmatic_details_md'
                ]
            }
        ),
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

class DemandCommissionAdmin(admin.ModelAdmin):
    search_fields = ['id']

admin.site.register(UnitOfMeasure, UnitOfMeasureAdmin)
admin.site.register(UOMRelationship)
admin.site.register(Supply, SupplyAdmin)
admin.site.register(Demand, DemandAdmin)
admin.site.register(SupplyQuote, SupplyQuoteAdmin)
admin.site.register(DemandQuote)
admin.site.register(ProductionCapability)
admin.site.register(Trench)
admin.site.register(Match, MatchAdmin)
admin.site.register(SupplyCommission, SupplyCommissionAdmin)
admin.site.register(DemandCommission, DemandCommissionAdmin)


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
