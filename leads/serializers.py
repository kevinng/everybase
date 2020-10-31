from rest_framework import serializers
from common.models import standard_fieldnames, choice_fieldnames
from .models import (Incoterm, Currency, PaymentMode, ContactType)

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