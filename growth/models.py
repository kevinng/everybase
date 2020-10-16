from django.db import models
from common.models import fk, m2m, m2mt, tf, cf, ff, dtf
from common.models import Standard, Choice

class GmassCampaignResult(Standard):
    email_address = models.EmailField(blank=True, null=True)
    first_name = cf(null=True)
    last_name = cf(null=True)
    name_1 = cf('Name_1', null=True)
    opens = cf(null=True)
    clicks = cf(null=True)
    replied = cf(null=True)
    unsubscribed = cf(null=True)
    bounced = cf(null=True)
    blocked = cf(null=True)
    over_gmail_limit = cf(null=True)
    bounce_reason = tf(null=True)
    gmail_response = cf(null=True)

    email = fk('relationships.Email', 'gmass_campaign_results')
    gmass_campaign = fk('GmassCampaign', 'results')

    def __str__(self):
        return '%s (%d)' % (self.email_address, self.id)

class GmassCampaign(Standard):
    campaign_id = cf()
    sent = dtf(null=True)
    subject = cf(null=True)
    spreadsheet = cf(null=True)

class ChemicalClusterOfSingaporeResult(Standard):
    sourced = dtf(null=True)
    source_link = models.URLField(blank=True, null=True)
    
    company_name = cf(null=True)
    telephone = cf(null=True)
    fax = cf(null=True)
    email_str = cf(null=True)
    website = models.URLField(blank=True, null=True)
    address_str = cf(null=True)

    company = fk('relationships.Company',
        'chemical_cluster_of_singapore_results', null=True)
    
    email = fk('relationships.Email',
        'chemical_cluster_of_singapore_results', null=True)

    phone_numbers = fk('relationships.PhoneNumber',
        'chemical_cluster_of_singapore_results', null=True)

    link = fk('relationships.Link',
        'chemical_cluster_of_singapore_results', null=True)

    address = fk('relationships.Address',
        'chemical_cluster_of_singapore_results', null=True)

    class Meta:
        verbose_name = 'ChemicalClusterOfSingapore result'
        verbose_name_plural = 'ChemicalClusterOfSingapore results'

class Fibre2FashionResult(Standard):
    sourced = dtf(null=True)

    source_link = cf(null=False)
    category = cf(null=False)
    sub_category = cf(null=False)
    email = cf(null=False)
    email_domain = cf(null=False)
    lead_type = cf(null=False)
    description = cf(null=False)

    links = m2m('relationships.Link', 'fibre2fashion_results', True)
    emails = m2m('relationships.Email', 'fibre2fashion_results', True)

    class Meta:
        verbose_name = 'Fibre2Fashion result'
        verbose_name_plural = 'Fibre2Fashion results'

class ZeroBounceResult(Standard):
    status = cf(null=False)
    sub_status = cf(null=False)
    account = cf(null=False)
    domain = cf(null=False)
    first_name = cf(null=False)
    last_name = cf(null=False)
    gender = cf(null=False)
    free_email = cf(null=False)
    mx_found = cf(null=False)
    mx_record = cf(null=False)
    smtp_provider = cf(null=False)
    did_you_mean = cf(null=False)

    email = fk('relationships.Email', 'zero_bounce_results', True)

    class Meta:
        verbose_name = 'ZeroBounce result'
        verbose_name_plural = 'ZeroBounce results'

class DataSource(Choice):
    emails = m2mt(
        'relationships.Email',
        'SourcedEmail',
        'source', 'email',
        'data_sources'
    )

class SourcedEmail(Standard):
    sourced = dtf(null=True)
    source = fk('DataSource', 'sourced_emails')
    email = fk('relationships.Email', 'sourced_emails')