from django.contrib import admin
from .models import (Incoterm, Currency, PaymentMode, ContactType, LeadCategory,
    MatchMethod, MatchStatus, SupplyQuoteStatus, DemandQuoteStatus,
    UnitOfMeasure, UOMRelationship, Supply, Demand, SupplyQuote, DemandQuote,
    ProductionCapability, Trench, Match, SupplyCommission, DemandCommission)
from common.admin import ChoiceAdmin

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

admin.site.register(Incoterm, ChoiceAdmin)
admin.site.register(Currency, ChoiceAdmin)
admin.site.register(PaymentMode, ChoiceAdmin)
admin.site.register(ContactType, ChoiceAdmin)
# admin.site.register(LeadCategory, ParentChildrenChoice) # Should be ParentChildrenChoiceAdmin
admin.site.register(MatchMethod, ChoiceAdmin)
admin.site.register(MatchStatus, ChoiceAdmin)
admin.site.register(SupplyQuoteStatus, ChoiceAdmin)
admin.site.register(DemandQuoteStatus, ChoiceAdmin)
admin.site.register(UnitOfMeasure, UnitOfMeasureAdmin)
admin.site.register(UOMRelationship)
admin.site.register(Supply)
admin.site.register(Demand)
admin.site.register(SupplyQuote)
admin.site.register(DemandQuote)
admin.site.register(ProductionCapability)
admin.site.register(Trench)
admin.site.register(Match)
admin.site.register(SupplyCommission)
admin.site.register(DemandCommission)