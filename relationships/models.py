from django.db import models
from common.models import fk, m2m, m2mt, tf, cf, dtf, pintf, eml, url
from common.models import (Standard, Choice, LowerCaseCharField,
    LowerCaseEmailField)

# --- Start: Abstract classes ---

relationship_fieldnames = ['details_md']
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
    
    def __str__(self):
        return f'({self.rtype}, {self.person}, {self.link} [{self.id}])'

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
        verbose_name = 'Person-company relationship'
        verbose_name_plural = 'Person-company relationships'

    def __str__(self):
        return f'({self.rtype}, {self.person}, {self.company} [{self.id}])'

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
        verbose_name = 'Person-address relationship'
        verbose_name_plural = 'Person-address relationships'

    def __str__(self):
        return f'({self.rtype}, {self.person}, {self.address} [{self.id}])'

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
        verbose_name = 'Person-phonenumber relationship'
        verbose_name_plural = 'Person-phonenumber relationships'

    def __str__(self):
        return f'({self.rtype}, {self.person}, {self.phone_number} [{self.id}])'

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
        verbose_name = 'Person-email relationship'
        verbose_name_plural = 'Person-email relationships'

    def __str__(self):
        return f'({self.rtype}, {self.person}, {self.email} [{self.id}])'

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
        verbose_name = 'Company-link relationship'
        verbose_name_plural = 'Company-link relationships'

    def __str__(self):
        return f'({self.rtype}, {self.company}, {self.link} [{self.id}])'

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
        verbose_name = 'Company-address relationship'
        verbose_name_plural = 'Company-address relationships'

    def __str__(self):
        return f'({self.rtype}, {self.company}, {self.address} [{self.id}])'

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
        verbose_name = 'Company-phonenumber relationship'
        verbose_name_plural = 'Company-phonenumber relationships'

    def __str__(self):
        return f'({self.rtype}, {self.company}, {self.phone_number} \
            [{self.id}])'

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
        verbose_name = 'Company-email relationship'
        verbose_name_plural = 'Company-email relationships'

    def __str__(self):
        return f'({self.rtype}, {self.company}, {self.email} [{self.id}])'

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

    def __str__(self):
        return f'({self.given_name}, {self.family_name}, {self.country} \
            [{self.id}])'

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
    
    def __str__(self):
        return f'({self.company_name} [{self.id}])'

class Email(Standard):
    email = LowerCaseEmailField(
        unique=True,
        null=False,
        blank=False,
        db_index=True
    )
    import_job = models.ForeignKey(
        'common.ImportJob',
        related_name='emails',
        related_query_name='emails',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )

    def __str__(self):
        return f'({self.email} [{self.id}])'

class InvalidEmail(Standard):
    email = LowerCaseCharField(
        max_length=500,
        unique=True,
        null=False,
        blank=False,
        db_index=True
    )
    import_job = models.ForeignKey(
        'common.ImportJob',
        related_name='invalid_emails',
        related_query_name='invalid_emails',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )

    def __str__(self):
        return f'({self.email} [{self.id}])'

class Link(Standard):
    verified = dtf(null=True)
    link = url()

    def __str__(self):
        return f'({self.link} [{self.id}])'

class Address(Standard):
    address_1 = cf()
    address_2 = cf(null=True)
    address_3 = cf(null=True)
    country = fk('common.Country', 'addresses')
    state = fk('common.State', 'addresses', null=True)
    postal_code = cf(null=True)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f'({self.address_1}, {self.country} [{self.id}])'

class PhoneNumberType(Choice):
    pass

class PhoneNumber(Standard):
    types = m2m('PhoneNumber', 'phone_numbers', True)
    country_code = pintf()
    national_number = pintf()

    def __str__(self):
        return f'(+{self.country_code} {self.national_number} [{self.id}])'

# --- End: Entities ---