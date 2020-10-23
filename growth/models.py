from django.db import models
from common.models import (fk, m2m, m2mt, tf, cf, ff, dtf, url, email, Standard,
    Choice, short_text)

# --- Start: Abstract classes ---

class Relationship(Standard):
    details_md = tf('Details in Markdown')

    class Meta:
        abstract = True

# --- End: Abstract classes ---

# --- Start: Relationships ---

class ChemicalBookResultLinkType(Choice):
    class Meta:
        verbose_name = 'ChemicalBookResult-Link Type'
        verbose_name_plural = 'ChemicalBookResult-Link Types'

class ChemicalBookResultLink(Relationship):
    rtype = fk('ChemicalBookResultLinkType',
        'chemicalbookresult_link_relationships',
        'ChemicalBookResult-Link Type')
    chemical_book_result = fk('ChemicalBookResult',
        'chemicalbookresult_link_relationships')
    link = fk('relationships.Link', 'chemicalbookresult_link_relationships')

    class Meta:
        verbose_name = 'ChemicalBookResult-Link Relationship'
        verbose_name_plural = 'ChemicalBookResult-Link Relationships'

    def __str__(self):
        return f'({self.rtype}, {self.chemical_book_result}, {self.link} \
            [{self.id}])'

class ChemicalBookResultCompanyType(Choice):
    class Meta:
        verbose_name = 'ChemicalBookResult-Company Type'
        verbose_name_plural = 'ChemicalBookResult-Company Types'

class ChemicalBookResultCompany(Relationship):
    rtype = fk('ChemicalBookResultCompanyType',
        'chemicalbookresult_company_relationships',
        'ChemicalBookResult-Company Type')
    chemical_book_result = fk('ChemicalBookResult',
        'chemicalbookresult_company_relationships')
    company = fk('relationships.Company',
        'chemicalbookresult_company_relationships')

    class Meta:
        verbose_name = 'ChemicalBookResult-Company Relationship'
        verbose_name_plural = 'ChemicalBookResult-Company Relationships'

    def __str__(self):
        return f'({self.rtype}, {self.chemical_book_result}, {self.company} \
            [{self.id}])'

class ChemicalBookResultPhoneNumberType(Choice):
    class Meta:
        verbose_name = 'ChemicalBookResult-PhoneNumber Type'
        verbose_name_plural = 'ChemicalBookResult-PhoneNumber Types'

class ChemicalBookResultPhoneNumber(Relationship):
    rtype = fk('ChemicalBookResultPhoneNumberType',
        'chemicalbookresult_phonenumber_relationships',
        'ChemicalBookResult-PhoneNumber Type')
    chemical_book_result = fk('ChemicalBookResult',
        'chemicalbookresult_phonenumber_relationships')
    phone_number = fk('relationships.PhoneNumber',
        'chemicalbookresult_phonenumber_relationships')

    class Meta:
        verbose_name = 'ChemicalBookResult-PhoneNumber Relationship'
        verbose_name_plural = 'ChemicalBookResult-PhoneNumber Relationships'

    def __str__(self):
        return f'({self.rtype}, {self.chemical_book_result}, \
            {self.phone_number} [{self.id}])'

class ChemicalBookResultEmailType(Choice):
    class Meta:
        verbose_name = 'ChemicalBookResult-Email Type'
        verbose_name_plural = 'ChemicalBookResult-Email Types'

class ChemicalBookResultEmail(Relationship):
    rtype = fk('ChemicalBookResultEmailType',
        'chemicalbookresult_email_relationships',
        'ChemicalBookResult-Email Type')
    chemical_book_result = fk('ChemicalBookResult',
        'chemicalbookresult_email_relationships')
    email = fk('relationships.Email', 'chemicalbookresult_email_relationships')

    class Meta:
        verbose_name = 'ChemicalBookResult-Email Relationship'
        verbose_name_plural = 'ChemicalBookResult-Email Relationships'

    def __str__(self):
        return f'({self.rtype}, {self.chemical_book_result}, \
            {self.email} [{self.id}])'

class ChemicalBookResultCountryType(Choice):
    class Meta:
        verbose_name = 'ChemicalBookResult-Country Type'
        verbose_name_plural = 'ChemicalBookResult-Country Types'

class ChemicalBookResultCountry(Relationship):
    rtype = fk('ChemicalBookResultCountryType',
        'chemicalbookresult_country_relationships',
        'ChemicalBookResult-Country Type')
    chemical_book_result = fk('ChemicalBookResult',
        'chemicalbookresult_country_relationships')
    country = fk('common.Country',
        'chemicalbookresult_country_relationships')

    class Meta:
        verbose_name = 'ChemicalBookResult-Country Relationship'
        verbose_name_plural = 'ChemicalBookResult-Country Relationships'

    def __str__(self):
        return f'({self.rtype}, {self.chemical_book_result}, \
            {self.country} [{self.id}])'

# --- End: Relationships ---

# --- Start: Growth models ---

class GmassCampaignResult(Standard):
    email_address = email(null=True)
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

    email = fk('relationships.Email',
        'gmass_campaign_results', null=True)
    gmass_campaign = fk('GmassCampaign',
        'results', null=True)

    def __str__(self):
        return f'({self.email_address} [{self.id}])'

class GmassCampaign(Standard):
    campaign_id = cf()
    sent = dtf(null=True)
    subject = cf(null=True)
    spreadsheet = cf(null=True)

    def __str__(self):
        return f'({self.campaign_id}, {self.sent} [{self.id}])'

class ChemicalClusterOfSingaporeResult(Standard):
    sourced = dtf(null=True)
    source_link = url(null=True)
    
    company_name = cf(null=True)
    telephone = cf(null=True)
    fax = cf(null=True)
    email_str = cf(null=True)
    website = url(null=True)
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

    def __str__(self):
        return f'({self.company_name}, {self.sourced} [{self.id}])'

class Fibre2FashionResult(Standard):
    sourced = dtf(null=True)

    source_link = url(null=False)
    category = cf(null=False)
    sub_category = cf(null=False)
    email = email(null=False)
    email_domain = cf(null=False)
    lead_type = cf(null=False)
    description = cf(null=False)

    links = m2m('relationships.Link', 'fibre2fashion_results', True)
    emails = m2m('relationships.Email', 'fibre2fashion_results', True)

    class Meta:
        verbose_name = 'Fibre2Fashion result'
        verbose_name_plural = 'Fibre2Fashion results'

    def __str__(self):
        return f'({short_text(self.source_link, backward=True)}, \
            {self.sourced} [{self.id}])'

class ZeroBounceResult(Standard):
    email_address = email(null=True)
    status = cf(null=True)
    sub_status = cf(null=True)
    account = cf(null=True)
    domain = cf(null=True)
    first_name = cf(null=True)
    last_name = cf(null=True)
    gender = cf(null=True)
    free_email = cf(null=True)
    mx_found = cf('MX found', null=True)
    mx_record = cf('MX record', null=True)
    smtp_provider = cf('SMTP provider', null=True)
    did_you_mean = cf('Did you mean?', null=True)

    email = fk('relationships.Email', 'zero_bounce_results', null=True)

    class Meta:
        verbose_name = 'ZeroBounce result'
        verbose_name_plural = 'ZeroBounce results'
    
    def __str__(self):
        return f'({self.email_address} [{self.id}])'

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

    def __str__(self):
        return f'({self.email_address} [{self.id}])'

class ChemicalBookResult(Standard):
    source_url = cf('Source URL', null=True)
    coy_name = cf('Company name', null=True)
    coy_internal_href = cf('Details page URL', null=True)
    coy_tel = cf('Company telephone', null=True)
    coy_email = cf('Company email', null=True)
    coy_href = cf('Company website', null=True)
    coy_nat = cf('Country', null=True)

    links = m2mt(
        'relationships.Link',
        'ChemicalBookResultLink',
        'chemical_book_result', 'link',
        'chemical_book_results'
    )

    companies = m2mt(
        'relationships.Company',
        'ChemicalBookResultCompany',
        'chemical_book_result', 'company',
        'chemical_book_results')

    phone_numbers = m2mt(
        'relationships.PhoneNumber',
        'ChemicalBookResultPhoneNumber',
        'chemical_book_result', 'phone_number',
        'chemical_book_results')

    emails = m2mt(
        'relationships.Email',
        'ChemicalBookResultEmail',
        'chemical_book_result', 'email',
        'chemical_book_results')

    countries = m2mt(
        'common.Country',
        'ChemicalBookResultCountry',
        'chemical_book_result', 'country',
        'chemical_book_results')

    class Meta:
        verbose_name = 'Chemical Book Result'
        verbose_name_plural = 'Chemical Book Results'

# --- End: Growth models ---