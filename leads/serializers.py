from rest_framework import serializers
from common.models import standard_fieldnames, choice_fieldnames
from .models import (expirable_invalidable_fieldnames, lead_fieldnames,
    commission_fieldnames, quote_fieldnames)
from .models import (Incoterm, Currency, PaymentMode, ContactType, LeadCategory,
    MatchMethod, MatchStatus, SupplyQuoteStatus, DemandQuoteStatus,
    UnitOfMeasure, UOMRelationship, Supply, Demand, SupplyQuote,
    ProductionCapability, DemandQuote, Trench, Match)

class IncotermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incoterm
        fields = ['id'] + choice_fieldnames

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id'] + choice_fieldnames

class PaymentModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMode
        fields = ['id'] + choice_fieldnames

class ContactTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactType
        fields = ['id'] + choice_fieldnames

class LeadCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadCategory
        fields = ['id'] + choice_fieldnames + ['parent']

class MatchMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchMethod
        fields = ['id'] + choice_fieldnames

class MatchStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchStatus
        fields = ['id'] + choice_fieldnames

class SupplyQuoteStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplyQuoteStatus
        fields = ['id'] + choice_fieldnames

class DemandQuoteStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandQuoteStatus
        fields = ['id'] + choice_fieldnames

class UnitOfMeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitOfMeasure
        fields = ['id'] + choice_fieldnames + ['category', 'parents']

class UOMRelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = UOMRelationship
        fields = ['id', 'child', 'parent', 'multiple', 'details_md']

class SupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Supply
        fields = ['id'] + standard_fieldnames + lead_fieldnames + \
            expirable_invalidable_fieldnames

class DemandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demand
        fields = ['id'] + standard_fieldnames + lead_fieldnames + \
            expirable_invalidable_fieldnames

class SupplyQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplyQuote
        fields = ['id'] + standard_fieldnames + quote_fieldnames + \
            expirable_invalidable_fieldnames + ['supply', 'status',
            'packing_details_md', 'downstreams', 'demand_quotes']

class ProductionCapabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionCapability
        fields = ['id'] + standard_fieldnames + ['supply_quote', 'start',
            'end', 'capacity_quantity', 'capacity_seconds', 'details_md']

class DemandQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandQuote
        fields = ['id'] + standard_fieldnames + quote_fieldnames + \
            expirable_invalidable_fieldnames + ['demand', 'status',
            'details_as_received_md', 'positive_origin_countries',
            'negative_origin_countries', 'negative_details_md']

class TrenchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trench
        fields = ['id', 'quantity', 'after_deposit_seconds', 'paymode',
            'payment_before_release', 'details_md', 'supply_quote',
            'demand_quote']

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['id'] + standard_fieldnames + ['demand_quote', 'supply_quote',
            'status', 'method', 'details_md']