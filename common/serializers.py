from rest_framework import serializers
from common.models import choice_fieldnames, standard_fieldnames
from . import models

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Country
        fields = ['id'] + choice_fieldnames + ['cc_tld']

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.State
        fields = ['id'] + choice_fieldnames + ['country']

class ImportJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ImportJob
        fields = ['id'] + standard_fieldnames + ['status']