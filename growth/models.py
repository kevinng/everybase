from django.db import models
from common.models import Standard, Choice

# --- Start: Helper lambda for model field declarations ---

# Foreign key
fk = lambda klass, name=None, verbose_name=None, null=False: models.ForeignKey(
    klass,
    on_delete=models.PROTECT,
    related_name=name,
    related_query_name=name,
    verbose_name=verbose_name,
    null=null,
    blank=null
)

# Many-to-many
m2m = lambda klass, name, blank=False: models.ManyToManyField(
    klass,
    related_name=name,
    related_query_name=name,
    blank=blank
)

# Many-to-many through
m2mt = lambda klass, thru, f1, f2, name: models.ManyToManyField(
    klass,
    through=thru,
    through_fields=(f1, f2),
    related_name=name,
    related_query_name=name
)

# Text
tf = lambda verbose_name=None, null=False: models.TextField(
    verbose_name=verbose_name, null=null, blank=null)

# Char
cf = lambda verbose_name=None, null=False: models.CharField(
    verbose_name=verbose_name, max_length=100, null=null, blank=null)

# Float
ff = lambda verbose_name=None, null=False: models.FloatField(
    verbose_name=verbose_name, null=null, blank=null)

# Datetime
dtf = lambda verbose_name=None, null=False, default=None: models.DateTimeField(
    null=null, blank=null, default=default)

# --- End: Helper lambda for model field declarations ---

class GmassCampaignResult(Standard):
    first_name = cf(null=True)
    last_name = cf(null=True)
    name_1 = cf(null=True)
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
    gmass_compaign = fk('GmassCampaign', 'results')

class GmassCampaign(Standard):
    campaign_id = cf(null=True)
    sent = dtf(null=True)
    subject = cf(null=True)
    spreadsheet = cf(null=True)

class ChemicalClusterOfSingaporeResult(Standard):
    sourced = dtf(null=True)
    
    company_name = cf(null=False)
    telephone = cf(null=False)
    fax = cf(null=False)
    email = cf(null=False)
    website = cf(null=False)
    source_link = cf(null=False)
    address = cf(null=False)

    company = fk('relationships.Company',
        'chemical_cluster_of_singapore_results')
    
    email = fk('relationships.Email',
        'chemical_cluster_of_singapore_results')

    phone_numbers = fk('relationships.PhoneNumber',
        'chemical_cluster_of_singapore_results')

    link = fk('relationships.Link',
        'chemical_cluster_of_singapore_results')

    address = fk('relationships.Address',
        'chemical_cluster_of_singapore_results')

class Fibre2FashionResult(Standard):
    sourced = dtf(null=True)

    source_link = cf(null=False)
    category = cf(null=False)
    sub_category = cf(null=False)
    email = cf(null=False)
    email_domain = cf(null=False)
    lead_type = cf(null=False)
    description = cf(null=False)

    links = m2m('relationships.Link', 'fibre2fashion_results')
    emails = m2m('relationships.Email', 'fibre2fashion_results')

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

    email = fk('relationships.Email', 'zero_bounce_results')

class DataSource(Choice):
    emails = m2mt(
        'relationships.Email',
        'SourcedEmail',
        'email', 'source',
        'data_sources'
    )

class SourcedEmail(Standard):
    sourced = dtf(null=True)
    source = fk('DataSource')
    email = fk('relationships.Email')