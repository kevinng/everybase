from django.db import models
from common.models import Standard, Choice

class GmassCampaignResult(Standard):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    name_1 = models.CharField(max_length=100)
    opens = models.CharField(max_length=100)
    clicks = models.CharField(max_length=100)
    replied = models.CharField(max_length=100)
    unsubscribed = models.CharField(max_length=100)
    bounced = models.CharField(max_length=100)
    blocked = models.CharField(max_length=100)
    over_gmail_limit = models.CharField(max_length=100)
    bounce_reason = models.TextField()
    gmail_response = models.CharField(max_length=100)

    email = models.ForeignKey(
        'relationships.Email',
        on_delete=models.PROTECT,
        related_name='gmass_campaign_results',
        related_query_name='gmass_campaign_results'
    )

    gmass_compaign = models.ForeignKey(
        'GmassCampaign',
        on_delete=models.PROTECT,
        related_name='results',
        related_query_name='results'
    )

class GmassCampaign(Standard):
    campaign_id = models.CharField(max_length=100)
    sent = models.DateTimeField(null=True, default=None)
    subject = models.CharField(max_length=100)
    spreadsheet = models.CharField(max_length=100)

class ChemicalClusterOfSingaporeResult(Standard):
    sourced = models.DateTimeField(null=True, default=None)
    
    company_name = models.CharField(max_length=100)
    telephone = models.CharField(max_length=100)
    fax = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    source_link = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    company = models.ForeignKey(
        'relationships.Company',
        on_delete=models.PROTECT,
        related_name='chemical_cluster_of_singapore_results',
        related_query_name='chemical_cluster_of_singapore_results'
    )
    
    email = models.ForeignKey(
        'relationships.Email',
        on_delete=models.PROTECT,
        related_name='chemical_cluster_of_singapore_results',
        related_query_name='chemical_cluster_of_singapore_results'
    )

    phone_numbers = models.ManyToManyField(
        'relationships.PhoneNumber',
        related_name='chemical_cluster_of_singapore_results',
        related_query_name='chemical_cluster_of_singapore_results'
    )

    link = models.ForeignKey(
        'relationships.Link',
        on_delete=models.PROTECT,
        related_name='chemical_cluster_of_singapore_results',
        related_query_name='chemical_cluster_of_singapore_results'
    )

    address = models.ForeignKey(
        'relationships.Address',
        on_delete=models.PROTECT,
        related_name='chemical_cluster_of_singapore_results',
        related_query_name='chemical_cluster_of_singapore_results'
    )

class Fibre2FashionResult(Standard):
    sourced = models.DateTimeField(null=True, default=None)

    source_link = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    email_domain = models.CharField(max_length=100)
    lead_type = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    links = models.ManyToManyField(
        'relationships.Link',
        related_name='fibre2fashion_results',
        related_query_name='fibre2fashion_results'
    )

    emails = models.ManyToManyField(
        'relationships.Email',
        related_name='fibre2fashion_results',
        related_query_name='fibre2fashion_results'
    )

class ZeroBounceResult(Standard):
    status = models.CharField(max_length=100)
    sub_status = models.CharField(max_length=100)
    account = models.CharField(max_length=100)
    domain = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    free_email = models.CharField(max_length=100)
    mx_found = models.CharField(max_length=100)
    mx_record = models.CharField(max_length=100)
    smtp_provider = models.CharField(max_length=100)
    did_you_mean = models.CharField(max_length=100)

    email = models.ForeignKey(
        'relationships.Email',
        on_delete=models.PROTECT,
        related_name='zero_bounce_results',
        related_query_name='zero_bounce_results'
    )

class DataSource(Choice):
    emails = models.ManyToManyField(
        'relationships.Email',
        through='SourcedEmail',
        through_fields=('email', 'source'),
        related_name='data_sources',
        related_query_name='data_sources'
    )

class SourcedEmail(Standard):
    sourced = models.DateTimeField(null=True, default=None)
    source = models.ForeignKey('DataSource', on_delete=models.PROTECT)
    email = models.ForeignKey('relationships.Email', on_delete=models.PROTECT)