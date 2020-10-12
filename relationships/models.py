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
rfk = lambda klass: models.ForeignKey(
        klass,
        on_delete=models.PROTECT,
        related_name='%(class)s_items',
        related_query_name='%(class)s_items'
    )

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
    rtype = rfk('PersonLinkType')
    person = rfk('Person')
    company = rfk('Company')

class PersonAddressType(Choice):
    pass

class PersonAddress(Relationship):
    rtype = rfk('PersonAddressType')
    person = rfk('Person')
    address = rfk('Address')

class PersonPhoneNumberType(Choice):
    pass

class PersonPhoneNumber(Relationship):
    rtype = rfk('PersonPhoneNumberType')
    person = rfk('Person')
    phone_number = rfk('PhoneNumber')

class PersonEmailType(Choice):
    pass

class PersonEmail(Relationship):
    rtype = rfk('PersonEmailType')
    person = rfk('Person')
    email = rfk('Email')

# --- End: Person Relationships ---

# --- Start: Company Relationships ---

class CompanyLinkType(Choice):
    pass

class CompanyLink(Relationship):
    rtype = rfk('CompanyLinkType')
    company = rfk('Company')
    link = rfk('Link')

class CompanyAddressType(Choice):
    pass

class CompanyAddress(Relationship):
    rtype = rfk('CompanyAddressType')
    company = rfk('Company')
    address = rfk('Address')

class CompanyPhoneNumberType(Choice):
    pass

class CompanyPhoneNumber(Relationship):
    rtype = rfk('CompanyPhoneNumberType')
    company = rfk('Company')
    phone_number = rfk('PhoneNumber')

class CompanyEmailType(Choice):
    pass

class CompanyEmail(Relationship):
    rtype = rfk('CompanyEmailType')
    company = rfk('Company')
    email = rfk('Email')

# --- End: Company Relationships ---

# --- Start: Entities ---

class Person(Standard):
    given_name = models.CharField(max_length=100)
    family_name = models.CharField(max_length=100)
    country = fk('common.Country', 'persons')
    state = fk('common.State', 'persons')
    notes_md = models.TextField()

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
    company_name = models.CharField(max_length=100)
    notes_md = models.TextField()

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
    last_visited_okay = models.DateTimeField(null=True, default=None)
    link = models.URLField()

class AddressType(Choice):
    pass

class Address(Standard):
    types = m2m('AddressType', 'addresses')
    address_1 = models.CharField(max_length=100)
    address_2 = models.CharField(max_length=100)
    address_3 = models.CharField(max_length=100)
    country = fk('common.Country', 'addresses')
    state = fk('common.State', 'addresses')
    postal_code = models.CharField(max_length=100)

class PhoneNumberType(Choice):
    pass

class PhoneNumber(Standard):
    types = m2m('PhoneNumber', 'phone_numbers')
    country_code = models.CharField(max_length=100)
    national_number = models.CharField(max_length=100)

# --- End: Entities ---