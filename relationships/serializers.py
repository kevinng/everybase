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

class PersonAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PersonAddress
        fields = ['id'] + relationship_fieldnames + ['rtype', 'person',
            'address']

class PersonPhoneNumberTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PersonPhoneNumberType
        fields = ['id'] + choice_fieldnames

class PersonPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PersonPhoneNumber
        fields = ['id'] + relationship_fieldnames + ['rtype', 'person',
            'phone_number']

class PersonEmailTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PersonEmailType
        fields = ['id'] + choice_fieldnames

class PersonEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PersonEmail
        fields = ['id'] + relationship_fieldnames + ['rtype', 'person', 'email']

class CompanyLinkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CompanyLinkType
        fields = ['id'] + choice_fieldnames

class CompanyAddressTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CompanyAddressType
        fields = ['id'] + choice_fieldnames

class CompanyAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CompanyAddress
        fields = ['id'] + relationship_fieldnames + ['rtype', 'company',
            'address']

class CompanyPhoneNumberTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CompanyPhoneNumberType
        fields = ['id'] + choice_fieldnames

class CompanyPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CompanyPhoneNumber
        fields = ['id'] + relationship_fieldnames + ['rtype', 'company',
            'phone_number']

class CompanyEmailTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CompanyEmailType
        fields = ['id'] + choice_fieldnames

class CompanyEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CompanyEmail
        fields = ['id'] + relationship_fieldnames + ['rtype', 'company',
            'email']

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Person
        fields = ['id'] + standard_fieldnames + ['given_name', 'family_name',
            'country', 'state', 'notes_md', 'companies', 'emails',
            'phone_numbers', 'addresses', 'links']

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = ['id'] + standard_fieldnames + ['company_name',
            'company_name_wo_postfix', 'notes_md', 'emails', 'phone_numbers',
            'addresses', 'links']