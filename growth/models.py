from django.db import models
from common.models import (fk, m2m, m2mt, tf, cf, ff, dtf, url, eml, Standard,
    Choice, short_text)

# --- Start: Abstract classes ---

class Relationship(Standard):
    details_md = tf('Details in Markdown', True)

    class Meta:
        abstract = True

# --- End: Abstract classes ---

# --- Start: Relationships ---

class ChemicalBookResultLinkType(Choice):
    class Meta:
        verbose_name = 'ChemicalBookResult-Link type'
        verbose_name_plural = 'ChemicalBookResult-Link types'

class ChemicalBookResultLink(Relationship):
    rtype = fk('ChemicalBookResultLinkType',
        'chemicalbookresult_link_relationships',
        'ChemicalBookResult-Link Type')
    chemical_book_result = fk('ChemicalBookResult',
        'chemicalbookresult_link_relationships')
    link = fk('relationships.Link', 'chemicalbookresult_link_relationships')

    class Meta:
        verbose_name = 'ChemicalBookResult-Link relationship'
        verbose_name_plural = 'ChemicalBookResult-Link relationships'

    def __str__(self):
        return f'({self.rtype}, {self.chemical_book_result}, {self.link} \
            [{self.id}])'

class ChemicalBookResultCompanyType(Choice):
    class Meta:
        verbose_name = 'ChemicalBookResult-Company type'
        verbose_name_plural = 'ChemicalBookResult-Company types'

class ChemicalBookResultCompany(Relationship):
    rtype = fk('ChemicalBookResultCompanyType',
        'chemicalbookresult_company_relationships',
        'ChemicalBookResult-Company Type')
    chemical_book_result = fk('ChemicalBookResult',
        'chemicalbookresult_company_relationships')
    company = fk('relationships.Company',
        'chemicalbookresult_company_relationships')

    class Meta:
        verbose_name = 'ChemicalBookResult-Company relationship'
        verbose_name_plural = 'ChemicalBookResult-Company relationships'

    def __str__(self):
        return f'({self.rtype}, {self.chemical_book_result}, {self.company} \
            [{self.id}])'

class ChemicalBookResultPhoneNumberType(Choice):
    class Meta:
        verbose_name = 'ChemicalBookResult-PhoneNumber type'
        verbose_name_plural = 'ChemicalBookResult-PhoneNumber types'

class ChemicalBookResultPhoneNumber(Relationship):
    rtype = fk('ChemicalBookResultPhoneNumberType',
        'chemicalbookresult_phonenumber_relationships',
        'ChemicalBookResult-PhoneNumber Type')
    chemical_book_result = fk('ChemicalBookResult',
        'chemicalbookresult_phonenumber_relationships')
    phone_number = fk('relationships.PhoneNumber',
        'chemicalbookresult_phonenumber_relationships')

    class Meta:
        verbose_name = 'ChemicalBookResult-PhoneNumber relationship'
        verbose_name_plural = 'ChemicalBookResult-PhoneNumber relationships'

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
        verbose_name = 'ChemicalBookResult-Email relationship'
        verbose_name_plural = 'ChemicalBookResult-Email relationships'

    def __str__(self):
        return f'({self.rtype}, {self.chemical_book_result}, \
            {self.email} [{self.id}])'

class ChemicalBookResultCountryType(Choice):
    class Meta:
        verbose_name = 'ChemicalBookResult-Country type'
        verbose_name_plural = 'ChemicalBookResult-Country types'

class ChemicalBookResultCountry(Relationship):
    rtype = fk('ChemicalBookResultCountryType',
        'chemicalbookresult_country_relationships',
        'ChemicalBookResult-Country Type')
    chemical_book_result = fk('ChemicalBookResult',
        'chemicalbookresult_country_relationships')
    country = fk('common.Country',
        'chemicalbookresult_country_relationships')

    class Meta:
        verbose_name = 'ChemicalBookResult-Country relationship'
        verbose_name_plural = 'ChemicalBookResult-Country relationships'

    def __str__(self):
        return f'({self.rtype}, {self.chemical_book_result}, \
            {self.country} [{self.id}])'

class LookChemResultCompanyType(Choice):
    class Meta:
        verbose_name = 'LookChemResult-Company type'
        verbose_name_plural = 'LookChemResult-Company types'

class LookChemResultCompany(Relationship):
    rtype = fk('LookChemResultCompanyType',
        'lookchemresult_company_relationships',
        'LookChemResult-Company Type')
    lookchem_result = fk('LookChemResult',
        'lookchemresult_company_relationships')
    company = fk('relationships.Company',
        'lookchemresult_company_relationships')
        
    class Meta:
        verbose_name = 'LookChemResult-Company relationship'
        verbose_name_plural = 'LookChemResult-Company relationships'

    def __str__(self):
        return f'({self.rtype}, {self.lookchem_result}, {self.company} \
            [{self.id}])'

class LookChemResultPersonType(Choice):
    class Meta:
        verbose_name = 'LookChemResult-Person type'
        verbose_name_plural = 'LookChemResult-Person types'

class LookChemResultPerson(Relationship):
    rtype = fk('LookChemResultPersonType',
        'lookchemresult_person_relationships',
        'LookChemResult-Person Type')
    lookchem_result = fk('LookChemResult',
        'lookchemresult_person_relationships')
    person = fk('relationships.Person',
        'lookchemresult_person_relationships')
        
    class Meta:
        verbose_name = 'LookChemResult-Person relationship'
        verbose_name_plural = 'LookChemResult-Person relationships'

    def __str__(self):
        return f'({self.rtype}, {self.lookchem_result}, {self.person} \
            [{self.id}])'

class LookChemResultAddressType(Choice):
    class Meta:
        verbose_name = 'LookChemResult-Address type'
        verbose_name_plural = 'LookChemResult-Address types'

class LookChemResultAddress(Relationship):
    rtype = fk('LookChemResultAddressType',
        'lookchemresult_address_relationships',
        'LookChemResult-Address Type')
    lookchem_result = fk('LookChemResult',
        'lookchemresult_address_relationships')
    address = fk('relationships.Address',
        'lookchemresult_address_relationships')
        
    class Meta:
        verbose_name = 'LookChemResult-Address relationship'
        verbose_name_plural = 'LookChemResult-Address relationships'

    def __str__(self):
        return f'({self.rtype}, {self.lookchem_result}, {self.address} \
            [{self.id}])'

class LookChemResultPhoneNumberType(Choice):
    class Meta:
        verbose_name = 'LookChemResult-PhoneNumber type'
        verbose_name_plural = 'LookChemResult-PhoneNumber types'

class LookChemResultPhoneNumber(Relationship):
    rtype = fk('LookChemResultPhoneNumberType',
        'lookchemresult_phonenumber_relationships',
        'LookChemResult-PhoneNumber Type')
    lookchem_result = fk('LookChemResult',
        'lookchemresult_phonenumber_relationships')
    phone_number = fk('relationships.PhoneNumber',
        'lookchemresult_phonenumber_relationships')
        
    class Meta:
        verbose_name = 'LookChemResult-PhoneNumber relationship'
        verbose_name_plural = 'LookChemResult-PhoneNumber relationships'

    def __str__(self):
        return f'({self.rtype}, {self.lookchem_result}, {self.phone_number} \
            [{self.id}])'

class LookChemResultEmailType(Choice):
    class Meta:
        verbose_name = 'LookChemResult-Email type'
        verbose_name_plural = 'LookChemResult-Email types'

class LookChemResultEmail(Relationship):
    rtype = fk('LookChemResultEmailType', 'lookchemresult_email_relationships',
        'LookChemResult-Email Type')
    lookchem_result = fk('LookChemResult', 'lookchemresult_email_relationships')
    email = fk('relationships.Email', 'lookchemresult_email_relationships')
        
    class Meta:
        verbose_name = 'LookChemResult-Email relationship'
        verbose_name_plural = 'LookChemResult-Email relationships'

    def __str__(self):
        return f'({self.rtype}, {self.lookchem_result}, {self.email} \
            [{self.id}])'

class LookChemResultLinkType(Choice):
    class Meta:
        verbose_name = 'LookChemResult-Link type'
        verbose_name_plural = 'LookChemResult-Link types'

class LookChemResultLink(Relationship):
    rtype = fk('LookChemResultEmailType', 'lookchemresult_link_relationships',
        'LookChemResult-Link Type')
    lookchem_result = fk('LookChemResult', 'lookchemresult_link_relationships')
    link = fk('relationships.Link', 'lookchemresult_link_relationships')
        
    class Meta:
        verbose_name = 'LookChemResult-Link relationship'
        verbose_name_plural = 'LookChemResult-Link relationships'

    def __str__(self):
        return f'({self.rtype}, {self.lookchem_result}, {self.link} \
            [{self.id}])'

class WorldOfChemicalsResultLinkType(Choice):
    class Meta:
        verbose_name = 'WorldOfChemicalsResult-Link type'
        verbose_name_plural = 'WorldOfChemicalsResult-Link types'

class WorldOfChemicalsResultLink(Relationship):
    rtype = fk('WorldOfChemicalsResultLinkType',
        'worldofchemicalsresult_link_relationships',
        'WorldOfChemicalsResult-Link Type')
    world_of_chemicals_result = fk('WorldOfChemicalsResult',
        'worldofchemicalsresult_link_relationships')
    link = fk('relationships.Link', 'worldofchemicalsresult_relationships')
        
    class Meta:
        verbose_name = 'WorldOfChemicalsResult-Link relationship'
        verbose_name_plural = 'WorldOfChemicalsResult-Link relationships'

    def __str__(self):
        return f'({self.rtype}, {self.world_of_chemicals_result}, {self.link} \
            [{self.id}])'

class WorldOfChemicalsResultCompanyType(Choice):
    class Meta:
        verbose_name = 'WorldOfChemicalsResult-Company type'
        verbose_name_plural = 'WorldOfChemicalsResult-Company types'

class WorldOfChemicalsResultCompany(Relationship):
    rtype = fk('WorldOfChemicalsResultCompanyType',
        'worldofchemicalsresult_company_relationships',
        'WorldOfChemicalsResult-Company Type')
    world_of_chemicals_result = fk('WorldOfChemicalsResult',
        'worldofchemicalsresult_company_relationships')
    company = fk('relationships.Company',
        'worldofchemicalsresult_relationships')
        
    class Meta:
        verbose_name = 'WorldOfChemicalsResult-Company relationship'
        verbose_name_plural = 'WorldOfChemicalsResult-Company relationships'

    def __str__(self):
        return f'({self.rtype}, {self.world_of_chemicals_result}, \
            {self.company} [{self.id}])'

class WorldOfChemicalsResultAddressType(Choice):
    class Meta:
        verbose_name = 'WorldOfChemicalsResult-Address type'
        verbose_name_plural = 'WorldOfChemicalsResult-Address types'

class WorldOfChemicalsResultAddress(Relationship):
    rtype = fk('WorldOfChemicalsResultAddressType',
        'worldofchemicalsresult_address_relationships',
        'WorldOfChemicalsResult-Address Type')
    world_of_chemicals_result = fk('WorldOfChemicalsResult',
        'worldofchemicalsresult_address_relationships')
    address = fk('relationships.Address',
        'worldofchemicalsresult_relationships')
        
    class Meta:
        verbose_name = 'WorldOfChemicalsResult-Address relationship'
        verbose_name_plural = 'WorldOfChemicalsResult-Address relationships'

    def __str__(self):
        return f'({self.rtype}, {self.world_of_chemicals_result}, \
            {self.address} [{self.id}])'

class WorldOfChemicalsResultPhoneNumberType(Choice):
    class Meta:
        verbose_name = 'WorldOfChemicalsResult-PhoneNumber type'
        verbose_name_plural = 'WorldOfChemicalsResult-PhoneNumber types'

class WorldOfChemicalsResultPhoneNumber(Relationship):
    rtype = fk('WorldOfChemicalsResultPhoneNumberType',
        'worldofchemicalsresult_phonenumber_relationships',
        'WorldOfChemicalsResult-PhoneNumber Type')
    world_of_chemicals_result = fk('WorldOfChemicalsResult',
        'worldofchemicalsresult_phonenumber_relationships')
    phone_number = fk('relationships.PhoneNumber',
        'worldofchemicalsresult_relationships')
        
    class Meta:
        verbose_name = 'WorldOfChemicalsResult-PhoneNumber relationship'
        verbose_name_plural = 'WorldOfChemicalsResult-PhoneNumber relationships'

    def __str__(self):
        return f'({self.rtype}, {self.world_of_chemicals_result}, \
            {self.phone_number} [{self.id}])'

class WorldOfChemicalsResultEmailType(Choice):
    class Meta:
        verbose_name = 'WorldOfChemicalsResult-Email type'
        verbose_name_plural = 'WorldOfChemicalsResult-Email types'

class WorldOfChemicalsResultEmail(Relationship):
    rtype = fk('WorldOfChemicalsResultEmailType',
        'worldofchemicalsresult_email_relationships',
        'WorldOfChemicalsResult-Email Type')
    world_of_chemicals_result = fk('WorldOfChemicalsResult',
        'worldofchemicalsresult_email_relationships')
    email = fk('relationships.Email', 'worldofchemicalsresult_relationships')
        
    class Meta:
        verbose_name = 'WorldOfChemicalsResult-Email relationship'
        verbose_name_plural = 'WorldOfChemicalsResult-Email relationships'

    def __str__(self):
        return f'({self.rtype}, {self.world_of_chemicals_result}, \
            {self.email} [{self.id}])'

# --- End: Relationships ---

# --- Start: Growth models ---

class GmassCampaignResult(Standard):
    email_address = cf(null=True)
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
    source_link = cf(null=True)
    
    company_name = cf(null=True)
    telephone = cf(null=True)
    fax = cf(null=True)
    email_str = cf(null=True)
    website = cf(null=True)
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

    def __str__(self):
        return f'({short_text(self.source_link, backward=True)}, \
            {self.sourced} [{self.id}])'

class ZeroBounceResult(Standard):
    email_address = cf(null=True)
    status = cf(null=True)
    sub_status = cf(null=True)
    account = cf(null=True)
    domain = cf(null=True)
    first_name = cf(null=True)
    last_name = cf(null=True)
    gender = cf(null=True)
    free_email = cf(null=True)
    mx_found = cf(null=True)
    mx_record = cf(null=True)
    smtp_provider = cf(null=True)
    did_you_mean = cf(null=True)

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
        'data_sources')

class SourcedEmail(Standard):
    sourced = dtf(null=True)
    source = fk('DataSource', 'sourced_emails')
    email = fk('relationships.Email', 'sourced_emails')

    def __str__(self):
        return f'({self.email_address} [{self.id}])'

class ChemicalBookResult(Standard):
    source_url = cf(null=True)
    coy_name = cf(null=True)
    coy_internal_href = cf(null=True)
    coy_tel = cf(null=True)
    coy_email = cf(null=True)
    coy_href = cf(null=True)
    coy_nat = cf(null=True)

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

    def __str__(self):
        return f'({self.coy_name} [{self.id}])'

class LookChemResult(Standard):
    coy_name = cf(null=True)
    contact_person = cf(null=True)
    street_address = cf(null=True)
    city = cf(null=True)
    province_state = cf(null=True)
    country_region = cf(null=True)
    zip_code = cf(null=True)
    business_type = cf(null=True)
    tel = cf(null=True)
    mobile = cf(null=True)
    email = cf(null=True)
    website = cf(null=True)
    qq = cf(null=True)

    companies = m2mt(
        'relationships.Company',
        'LookChemResultCompany',
        'lookchem_result', 'company',
        'lookchem_results')
    
    persons = m2mt(
        'relationships.Person',
        'LookChemResultPerson',
        'lookchem_result', 'person',
        'lookchem_results')

    addresses = m2mt(
        'relationships.Address',
        'LookChemResultAddress',
        'lookchem_result', 'address',
        'lookchem_results')

    phone_numbers = m2mt(
        'relationships.PhoneNumber',
        'LookChemResultPhoneNumber',
        'lookchem_result', 'phone_number',
        'lookchem_results')

    emails = m2mt(
        'relationships.Email',
        'LookChemResultEmail',
        'lookchem_result', 'email',
        'lookchem_results')

    links = m2mt(
        'relationships.Link',
        'LookChemResultLink',
        'lookchem_result', 'link',
        'lookchem_results')

    def __str__(self):
        return f'({self.coy_name} [{self.id}])'

class WorldOfChemicalsResult(Standard):
    source_url = cf(null=True)
    coy_id = cf(null=True)
    coy_name = cf(null=True)
    coy_about_html = tf(null=True)
    coy_pri_contact = cf(null=True)
    coy_addr_1 = cf(null=True)
    coy_addr_2 = cf(null=True)
    coy_city = cf(null=True)
    coy_state = cf(null=True)
    coy_country = cf(null=True)
    coy_postal = cf(null=True)
    coy_phone = cf(null=True)
    coy_phone_2 = cf(null=True)
    coy_email = cf(null=True)
    coy_owner_email = cf(null=True)
    coy_alt_email = cf(null=True)
    coy_alt_email_2 = cf(null=True)
    coy_alt_email_3 = cf(null=True)
    coy_website = cf(null=True)

    links = m2mt(
        'relationships.Link',
        'WorldOfChemicalsResultLink',
        'world_of_chemicals_result', 'link',
        'world_of_chemcials_results')

    companies = m2mt(
        'relationships.Company',
        'WorldOfChemicalsResultCompany',
        'world_of_chemicals_result', 'company',
        'world_of_chemcials_results')

    addresses = m2mt(
        'relationships.Address',
        'WorldOfChemicalsResultAddress',
        'world_of_chemicals_result', 'address',
        'world_of_chemcials_results')

    phone_numbers = m2mt(
        'relationships.PhoneNumber',
        'WorldOfChemicalsResultPhoneNumber',
        'world_of_chemicals_result', 'phone_number',
        'world_of_chemcials_results')

    emails = m2mt(
        'relationships.Email',
        'WorldOfChemicalsResultEmail',
        'world_of_chemicals_result', 'email',
        'world_of_chemcials_results')
    
    def __str__(self):
        return f'({self.coy_name} [{self.id}])'

# --- End: Growth models ---