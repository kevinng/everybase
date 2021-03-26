from rest_framework import serializers
from common.models import standard_fieldnames, choice_fieldnames
from . import models

class PhoneNumberTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PhoneNumberType
        fields = ['id'] + choice_fieldnames

class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PhoneNumber
        fields = ['id'] + standard_fieldnames + ['types', 'country_code',
            'national_number']

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Email
        fields = ['id'] + standard_fieldnames + ['email', 'import_job']

class InvalidEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InvalidEmail
        fields = ['id'] + standard_fieldnames + ['email', 'import_job']