from django.db import models
from common.models import fk, m2m, m2mt, tf, cf, ff, dtf
from common.models import Standard, Choice

# --- Start: Abstract classes ---

class Relationship(Standard):
    details_md = tf('Details in Markdown')

    class Meta:
        abstract = True

# --- End: Abstract classes ---

# --- Start: Person Relationships ---

class PersonLinkType(Choice):
    class Meta:
        verbose_name = 'Person-link type'
        verbose_name_plural = 'Person-link types'

class PersonLink(Relationship):
    rtype = fk('PersonLinkType', 'person_link_relationships',
        'Person-link relationship type')
    person = fk('Person', 'person_link_relationships')
    link = fk('Link', 'person_link_relationships')

    class Meta:
        verbose_name = 'Person-link'
        verbose_name_plural = 'Person-links'

class PersonCompanyType(Choice):
    class Meta:
        verbose_name = 'Person-company type'
        verbose_name_plural = 'Person-company types'

class PersonCompany(Relationship):
    rtype = fk('PersonCompanyType', 'person_company_relationships',
        'Person-company relationship type')
    person = fk('Person', 'persons')
    company = fk('Company', 'companies')

    class Meta:
        verbose_name = 'Person-company'
        verbose_name_plural = 'Person-companies'

class PersonAddressType(Choice):
    class Meta:
        verbose_name = 'Person-address type'
        verbose_name_plural = 'Person-address types'

class PersonAddress(Relationship):
    rtype = fk('PersonAddressType', 'person_address_relationships',
        'Person-address relationship type')
    person = fk('Person', 'person_address_relationships')
    address = fk('Address', 'person_address_relationships')

    class Meta:
        verbose_name = 'Person-address'
        verbose_name_plural = 'Person-addresses'

class PersonPhoneNumberType(Choice):
    class Meta:
        verbose_name = 'Person-phonenumber type'
        verbose_name_plural = 'Person-phonenumber types'

class PersonPhoneNumber(Relationship):
    rtype = fk('PersonPhoneNumberType', 'person_phonenumber_relationships',
        'Person-phonenumber relationship type')
    person = fk('Person', 'person_phonenumber_relationships')
    phone_number = fk('PhoneNumber', 'person_phonenumber_relationships')

    class Meta:
        verbose_name = 'Person-phonenumber'
        verbose_name_plural = 'Person-phonenumbers'

class PersonEmailType(Choice):
    class Meta:
        verbose_name = 'Person-email type'
        verbose_name_plural = 'Person-email types'

class PersonEmail(Relationship):
    rtype = fk('PersonEmailType', 'person_email_relationships',
        'Person-email relationship type')
    person = fk('Person', 'person_email_relationships')
    email = fk('Email', 'person_email_relationships')

    class Meta:
        verbose_name = 'Person-email'
        verbose_name_plural = 'Person-emails'

# --- End: Person Relationships ---

# --- Start: Company Relationships ---

class CompanyLinkType(Choice):
    class Meta:
        verbose_name = 'Company-link type'
        verbose_name_plural = 'Company-link types'

class CompanyLink(Relationship):
    rtype = fk('CompanyLinkType', 'company_link_relationships',
        'Company-link relationship type')
    company = fk('Company', 'company_link_relationships')
    link = fk('Link', 'company_link_relationships')

    class Meta:
        verbose_name = 'Company-link'
        verbose_name_plural = 'Company-links'

class CompanyAddressType(Choice):
    class Meta:
        verbose_name = 'Company-address type'
        verbose_name_plural = 'Company-address types'

class CompanyAddress(Relationship):
    rtype = fk('CompanyAddressType', 'company_address_relationships',
        'Company-address relationship type')
    company = fk('Company', 'company_address_relationships')
    address = fk('Address', 'company_address_relationships')

    class Meta:
        verbose_name = 'Company-address'
        verbose_name_plural = 'Company-addresses'

class CompanyPhoneNumberType(Choice):
    class Meta:
        verbose_name = 'Company-phonenumber types'
        verbose_name_plural = 'Company-phonenumber types'

class CompanyPhoneNumber(Relationship):
    rtype = fk('CompanyPhoneNumberType', 'company_phonenumber_relationships',
        'Company-phonenumber relationship type')
    company = fk('Company', 'company_phonenumber_relationships')
    phone_number = fk('PhoneNumber', 'company_phonenumber_relationships')

    class Meta:
        verbose_name = 'Company-phonenumber'
        verbose_name_plural = 'Company-phonenumbers'

class CompanyEmailType(Choice):
    class Meta:
        verbose_name = 'Company-email type'
        verbose_name_plural = 'Company-email types'

class CompanyEmail(Relationship):
    rtype = fk('CompanyEmailType', 'company_email_relationships',
        'Company-email relationship type')
    company = fk('Company', 'company_email_relationships')
    email = fk('Email', 'company_email_relationships')

    class Meta:
        verbose_name = 'Company-email'
        verbose_name_plural = 'Company-emails'

# --- End: Company Relationships ---

# --- Start: Entities ---

class Person(Standard):
    given_name = cf(null=True)
    family_name = cf(null=True)
    country = fk('common.Country', 'persons', null=True)
    state = fk('common.State', 'persons', null=True)
    notes_md = tf('Notes in Markdown', null=True)

    companies = m2mt(
        'Company',
        'PersonCompany',
        'person', 'company',
        'persons'
    )

    emails = m2mt(
        'Email',
        'PersonEmail',
        'person', 'email',
        'persons'
    )

    phone_numbers = m2mt(
        'PhoneNumber',
        'PersonPhoneNumber',
        'person', 'phone_number',
        'persons'
    )

    addresses = m2mt(
        'Address',
        'PersonAddress',
        'person', 'address',
        'persons'
    )

    links = m2mt(
        'Link',
        'PersonLink',
        'person', 'link',
        'persons'
    )

class Company(Standard):
    company_name = cf()
    company_name_wo_postfix = cf()
    notes_md = tf('Notes in Markdown', True)

    emails = m2mt(
        'Email',
        'CompanyEmail',
        'company', 'email',
        'companies'
    )

    phone_numbers = m2mt(
        'PhoneNumber',
        'CompanyPhoneNumber',
        'company', 'phone_number',
        'companies'
    )

    addresses = m2mt(
        'Address',
        'CompanyAddress',
        'company', 'address',
        'companies'
    )

    links = m2mt(
        'Link',
        'CompanyLink',
        'company', 'link',
        'companies'
    )

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

class Email(Standard):
    email = models.EmailField()

class LinkType(Choice):
    pass

class Link(Standard):
    last_visited_okay = dtf(null=True)

    types = m2m('LinkType', 'links', True)
    link = models.URLField()

class AddressType(Choice):
    pass

class Address(Standard):
    types = m2m('AddressType', 'addresses', True)
    address_1 = cf()
    address_2 = cf(null=True)
    address_3 = cf(null=True)
    country = fk('common.Country', 'addresses')
    state = fk('common.State', 'addresses', null=True)
    postal_code = cf(null=True)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

class PhoneNumberType(Choice):
    pass

class PhoneNumber(Standard):
    types = m2m('PhoneNumber', 'phone_numbers', True)
    country_code = cf()
    national_number = cf()

# --- End: Entities ---