from rest_framework import serializers
from common.models import standard_fieldnames, choice_fieldnames
from .models import relationship_fieldnames
from . import models

class PersonLinkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PersonLinkType
        fields = ['id'] + choice_fieldnames

class PersonLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PersonLink
        fields = ['id'] + relationship_fieldnames + ['rtype', 'person', 'link']

class PersonCompanyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PersonCompanyType
        fields = ['id'] + choice_fieldnames

class PersonCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PersonCompany
        fields = ['id'] + relationship_fieldnames + ['rtype', 'person',
            'company']

class PersonAddressTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PersonAddressType
        fields = ['id'] + choice_fieldnames