from rest_framework import serializers
from common.models import standard_fieldnames, choice_fieldnames
from . import models

class GmassCampaignResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GmassCampaignResult
        fields = ['id'] + standard_fieldnames + ['email_address', 'first_name',
            'last_name', 'name_1', 'opens', 'clicks', 'replied',
            'unsubscribed', 'bounced', 'blocked', 'over_gmail_limit',
            'bounce_reason', 'gmail_response', 'email', 'gmass_campaign']

class GmassCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GmassCampaign
        fields = ['id'] + standard_fieldnames + ['campaign_id', 'sent',
            'subject', 'spreadsheet']

class ChemicalClusterOfSingaporeResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChemicalClusterOfSingaporeResult
        fields = ['id'] + standard_fieldnames + ['sourced', 'source_link',
            'company_name', 'telephone', 'fax', 'email_str', 'website',
            'address_str', 'company', 'email', 'phone_numbers', 'link',
            'address']

# class Fibre2FashionResultSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Fibre2FashionResult
#         fields = ['id'] + standard_fieldnames + ['sourced', 'source_link',
#             'category', 'sub_category', 'email', 'email_domain', 'lead_type',
#             'description', 'links', 'emails']

class ZeroBounceResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ZeroBounceResult
        fields = ['id'] + standard_fieldnames + ['import_job', 'generated',
            'email_str', 'status', 'sub_status', 'account', 'domain',
            'first_name', 'last_name', 'gender', 'free_email', 'mx_found',
            'mx_record', 'smtp_provider', 'did_you_mean', 'email',
            'invalid_email', 'did_you_mean_email']

class DataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DataSource
        fields = ['id'] + choice_fieldnames + ['emails']

class SourcedEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SourcedEmail
        fields = ['id'] + standard_fieldnames + ['sourced', 'source', 'email']

class ChemicalBookResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChemicalBookResult
        fields = ['id'] + standard_fieldnames + ['source_url', 'coy_name',
            'coy_internal_href', 'coy_tel', 'coy_email', 'coy_href', 'coy_nat',
            'links', 'companies', 'phone_numbers', 'countries']

class LookChemResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LookChemResult
        fields = ['id'] + standard_fieldnames + ['coy_name', 'contact_person',
            'street_address', 'city', 'province_state', 'country_region',
            'zip_code', 'business_type', 'tel', 'mobile', 'email', 'website',
            'qq', 'companies', 'persons', 'addresses', 'phone_numbers',
            'emails', 'links']

class WorldOfChemicalResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WorldOfChemicalsResult
        fields = ['id'] + standard_fieldnames + ['coy_id', 'coy_name',
            'coy_about_html', 'coy_pri_contact', 'coy_addr_1', 'coy_addr_2',
            'coy_city', 'coy_state', 'coy_country', 'coy_postal', 'coy_phone',
            'coy_phone_2', 'coy_email', 'coy_owner_email', 'coy_alt_email',
            'coy_alt_email_2', 'coy_alt_email_3', 'coy_website']