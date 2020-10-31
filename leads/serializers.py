from rest_framework import serializers
from common.models import standard_fieldnames, choice_fieldnames
from .models import (Incoterm, Currency, PaymentMode, ContactType, LeadCategory,
    MatchMethod, MatchStatus, SupplyQuoteStatus, DemandQuoteStatus)

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