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

# --- Start: Abstract ---

# Helper function to declare foreign key relationships in relationship classes.
# rfk = lambda klass: models.ForeignKey(
#         klass,
#         on_delete=models.PROTECT,
#         related_name='%(class)s_items',
#         related_query_name='%(class)s_items'
#     )

# # Helper function to declare foreign key relationships.
# fk = lambda klass, name: models.ForeignKey(
#         klass,
#         on_delete=models.PROTECT,
#         related_name=name,
#         related_query_name=name
#     )

# # Helper function to declare many-to-many relationships.
# m2m = lambda klass, name: models.ManyToManyField(
#         klass,
#         related_name=name,
#         related_query_name=name
#     )

# # Helper function to declare many-to-many through relationships.
# m2mt = lambda klass, thru, f1, f2, name: models.ManyToManyField(
#         klass,
#         through=thru,
#         through_fields=(f1, f2),
#         related_name=name,
#         related_query_name=name
#     )

class Relationship(models.Model):
    details_md = tf('Details in Markdown')

    class Meta:
        abstract = True

# --- End: Abstract ---

# --- Start: Person Relationships ---

class PersonLinkType(Choice):
    pass

class PersonLink(Relationship):
    rtype = fk('PersonLinkType', 'person_link_relationships',
        'Person-link relationship type')
    person = fk('Person', 'person_link_relationships')
    link = fk('Link', 'person_link_relationships')

class PersonCompanyType(Choice):
    pass

class PersonCompany(Relationship):
    rtype = fk('PersonCompanyType', 'person_company_relationships',
        'Person-company relationship type')
    person = fk('Person', 'persons')
    company = fk('Company', 'companies')

class PersonAddressType(Choice):
    pass

class PersonAddress(Relationship):
    rtype = fk('PersonAddressType', 'person_address_relationships',
        'Person-address relationship type')
    person = fk('Person', 'person_address_relationships')
    address = fk('Address', 'person_address_relationships')

class PersonPhoneNumberType(Choice):
    pass

class PersonPhoneNumber(Relationship):
    rtype = fk('PersonPhoneNumberType', 'person_phonenumber_relationships',
        'Person-phonenumber relationship type')
    person = fk('Person', 'person_phonenumber_relationships')
    phone_number = fk('PhoneNumber', 'person_phonenumber_relationships')

class PersonEmailType(Choice):
    pass

class PersonEmail(Relationship):
    rtype = fk('PersonEmailType', 'person_email_relationships',
        'Person-email relationship type')
    person = fk('Person', 'person_email_relationships')
    email = fk('Email', 'person_email_relationships')

# --- End: Person Relationships ---

# --- Start: Company Relationships ---

class CompanyLinkType(Choice):
    pass

class CompanyLink(Relationship):
    rtype = fk('CompanyLinkType', 'company_link_relationships',
        'Company-link relationship type')
    company = fk('Company', 'company_link_relationships')
    link = fk('Link', 'company_link_relationships')

class CompanyAddressType(Choice):
    pass

class CompanyAddress(Relationship):
    rtype = fk('CompanyAddressType', 'company_address_relationships',
        'Company-address relationship type')
    company = fk('Company', 'company_address_relationships')
    address = fk('Address', 'company_address_relationships')

class CompanyPhoneNumberType(Choice):
    pass

class CompanyPhoneNumber(Relationship):
    rtype = fk('CompanyPhoneNumberType', 'company_phonenumber_relationships',
        'Company-phonenumber relationship type')
    company = fk('Company', 'company_phonenumber_relationships')
    phone_number = fk('PhoneNumber', 'company_phonenumber_relationships')

class CompanyEmailType(Choice):
    pass

class CompanyEmail(Relationship):
    rtype = fk('CompanyEmailType', 'company_email_relationships',
        'Company-email relationship type')
    company = fk('Company', 'company_email_relationships')
    email = fk('Email', 'company_email_relationships')

# --- End: Company Relationships ---

# --- Start: Entities ---

class Person(Standard):
    given_name = cf()
    family_name = cf()
    country = fk('common.Country', 'persons')
    state = fk('common.State', 'persons')
    notes_md = tf('Notes in Markdown', True)

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
    notes_md = tf('Notes in Markdown')

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

class Email(Standard):
    email = models.EmailField()

class LinkType(Choice):
    pass

class Link(Standard):
    types = m2m('LinkType', 'links')
    last_visited_okay = dtf()
    link = models.URLField()

class AddressType(Choice):
    pass

class Address(Standard):
    types = m2m('AddressType', 'addresses')
    address_1 = cf()
    address_2 = cf()
    address_3 = cf()
    country = fk('common.Country', 'addresses')
    state = fk('common.State', 'addresses')
    postal_code = cf()

class PhoneNumberType(Choice):
    pass

class PhoneNumber(Standard):
    types = m2m('PhoneNumber', 'phone_numbers')
    country_code = models.CharField(max_length=100)
    national_number = models.CharField(max_length=100)

# --- End: Entities ---