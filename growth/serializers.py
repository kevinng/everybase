from rest_framework import serializers
from common.models import standard_fieldnames, choice_fieldnames
from .models import (GmassCampaignResult, GmassCampaign,
    ChemicalClusterOfSingaporeResult, Fibre2FashionResult, ZeroBounceResult,
    DataSource, SourcedEmail, ChemicalBookResult, LookChemResult)

class GmassCampaignResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = GmassCampaignResult
        fields = ['id'] + standard_fieldnames + ['email_address', 'first_name',
            'last_name', 'name_1', 'opens', 'clicks', 'replied',
            'unsubscribed', 'bounced', 'blocked', 'over_gmail_limit',
            'bounce_reason', 'gmail_response', 'email', 'gmass_campaign']

class GmassCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = GmassCampaign
        fields = ['id'] + standard_fieldnames + ['campaign_id', 'sent',
            'subject', 'spreadsheet']

class ChemicalClusterOfSingaporeResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChemicalClusterOfSingaporeResult
        fields = ['id'] + standard_fieldnames + ['sourced', 'source_link',
            'company_name', 'telephone', 'fax', 'email_str', 'website',
            'address_str', 'company', 'email', 'phone_numbers', 'link',
            'address']

class Fibre2FashionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fibre2FashionResult
        fields = ['id'] + standard_fieldnames + ['sourced', 'source_link',
            'category', 'sub_category', 'email', 'email_domain', 'lead_type',
            'description', 'links', 'emails']

class ZeroBounceResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZeroBounceResult
        fields = ['id'] + standard_fieldnames + ['email_address', 'status',
            'sub_status', 'account', 'domain', 'first_name', 'last_name',
            'gender', 'free_email', 'mx_found', 'mx_record', 'smtp_provider',
            'did_you_mean', 'email']

class DataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSource
        fields = ['id'] + choice_fieldnames + ['emails']

class SourcedEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourcedEmail
        fields = ['id'] + standard_fieldnames + ['sourced', 'source', 'email']

class ChemicalBookResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChemicalBookResult
        fields = ['id'] + standard_fieldnames + ['source_url', 'coy_name',
            'coy_internal_href', 'coy_tel', 'coy_email', 'coy_href', 'coy_nat',
            'links', 'companies', 'phone_numbers', 'countries']

class LookChemResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = LookChemResult
        fields = ['id'] + standard_fieldnames + ['coy_name', 'contact_person',
            'street_address', 'city', 'province_state', 'country_region',
            'zip_code', 'business_type', 'tel', 'mobile', 'email', 'website',
            'qq', 'companies', 'persons', 'addresses', 'phone_numbers',
            'emails', 'links']