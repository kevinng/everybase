from rest_framework import serializers
from common.models import standard_fieldnames, choice_fieldnames
from . import models

class GmassCampaignResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GmassCampaignResult
        fields = ['id'] + standard_fieldnames + ['email_address', 'first_name',
            'last_name', 'name_1', 'opens', 'clicks', 'replied',
            'unsubscribed', 'bounced', 'blocked', 'over_gmail_limit',
            'bounce_reason', 'gmail_response', 'email', 'invalid_email',
            'gmass_campaign']

class GmassCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GmassCampaign
        fields = ['id'] + standard_fieldnames + ['campaign_id', 'sent',
            'subject', 'spreadsheet']

class ChemicalClusterOfSingaporeCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChemicalClusterOfSingaporeCompany
        fields = ['id'] + standard_fieldnames + ['import_job', 'harvested',
            'source_url', 'company_name', 'telephone', 'fax', 'email_str',
            'website', 'address', 'nature_of_business', 'executive_name',
            'executive_telephone', 'executive_email_str', 'email',
            'invalid_email', 'executive_email', 'invalid_executive_email']

class ChemicalClusterOfSingaporeProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChemicalClusterOfSingaporeCompany
        fields = ['id'] + standard_fieldnames + ['import_job', 'harvested',
            'source_url', 'company_name', 'product']

class ChemicalClusterOfSingaporeServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChemicalClusterOfSingaporeCompany
        fields = ['id'] + standard_fieldnames + ['import_job', 'harvested',
            'source_url', 'company_name', 'service']

class Fibre2FashionBuyingOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Fibre2FashionBuyingOffer
        fields = ['id'] + standard_fieldnames + ['import_job', 'harvested',
            'source_url', 'category', 'sub_category', 'title', 'reference_no',
            'description', 'email_str', 'product_info_html', 'email',
            'invalid_email']

class Fibre2FashionSellingOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Fibre2FashionSellingOffer
        fields = ['id'] + standard_fieldnames + ['import_job', 'harvested',
            'source_url', 'category', 'sub_category', 'title', 'reference_no',
            'description', 'email_str', 'company_name', 'company_address',
            'product_info_html', 'email', 'invalid_email']

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

class ChemicalBookSupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChemicalBookSupplier
        fields = ['id'] + standard_fieldnames + ['import_job', 'harvested',
            'source_url', 'company_name', 'internal_url', 'telephone',
            'email_str', 'corporate_site_url', 'nationality', 'email',
            'invalid_email']

class LookChemSupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LookChemSupplier
        fields = ['id'] + standard_fieldnames + ['company_name',
            'contact_person', 'street_address', 'city', 'province_state',
            'country_region', 'zip_code', 'business_type', 'tel', 'mobile',
            'email_str', 'website', 'qq', 'email', 'invalid_email']

class WorldOfChemicalSupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WorldOfChemicalsSupplier
        fields = ['id'] + standard_fieldnames + ['coy_id', 'coy_name',
            'coy_about_html', 'coy_pri_contact', 'coy_addr_1', 'coy_addr_2',
            'coy_city', 'coy_state', 'coy_country', 'coy_postal', 'coy_phone',
            'coy_phone_2', 'coy_email', 'coy_owner_email', 'coy_alt_email',
            'coy_alt_email_2', 'coy_alt_email_3', 'coy_website', 'email',
            'owner_email', 'alt_email', 'alt_email_2', 'alt_email_3',
            'invalid_email', 'invalid_owner_email', 'invalid_alt_email',
            'invalid_alt_email_2', 'invalid_alt_email_3']

class OKChemBuyingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OKChemBuyingRequest
        fields = ['id'] + standard_fieldnames + ['harvested', 'name', 'country',
            'request', 'email', 'domain']