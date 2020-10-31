from rest_framework import serializers
from common.models import standard_fieldnames, choice_fieldnames
from .models import (Incoterm, Currency)

class IncotermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incoterm
        fields = ['id'] + choice_fieldnames

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id'] + choice_fieldnames