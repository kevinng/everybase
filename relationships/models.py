from django.db import models
from common.models import (Standard, Choice, LowerCaseCharField,
    LowerCaseEmailField)

# --- Start: Abstract classes ---

relationship_fieldnames = ['details_md']
class Relationship(Standard):
    details_md = models.TextField(
        verbose_name='Details in Markdown',
        null=False,
        blank=False
    )

    class Meta:
        abstract = True

# --- End: Abstract classes ---

# --- Start: Person Relationships ---

class PersonLinkType(Choice):
    class Meta:
        verbose_name = 'Person-link type'
        verbose_name_plural = 'Person-link types'

class PersonLink(Relationship):
    rtype = models.ForeignKey(
        'PersonLinkType',
        on_delete=models.PROTECT,
        related_name='person_link_relationships',
        related_query_name='person_link_relationships',
        verbose_name='Person-link relationship type',
        null=False,
        blank=False,
        db_index=True
    )
    person = models.ForeignKey(
        'Person',
        on_delete=models.PROTECT,
        related_name='person_link_relationships',
        related_query_name='person_link_relationships',
        null=False,
        blank=False,
        db_index=True
    )
    link = models.ForeignKey(
        'Link',
        on_delete=models.PROTECT,
        related_name='person_link_relationships',
        related_query_name='person_link_relationships',
        null=False,
        blank=False,
        db_index=True
    )

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
    rtype = models.ForeignKey(
        'PersonCompanyType',
        on_delete=models.PROTECT,
        related_name='person_company_relationships',
        related_query_name='person_company_relationships',
        verbose_name='Person-company relationship type',
        null=False,
        blank=False,
        db_index=True
    )
    person = models.ForeignKey(
        'Person',
        on_delete=models.PROTECT,
        related_name='persons',
        related_query_name='persons',
        null=False,
        blank=False,
        db_index=True
    )
    company = models.ForeignKey(
        'Company',
        on_delete=models.PROTECT,
        related_name='companies',
        related_query_name='companies',
        null=False,
        blank=False,
        db_index=True
    )

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
    rtype = models.ForeignKey(
        'PersonAddressType',
        on_delete=models.PROTECT,
        related_name='person_address_relationships',
        related_query_name='person_address_relationships',
        verbose_name='Person-address relationship type',
        null=False,
        blank=False,
        db_index=True
    )
    person = models.ForeignKey(
        'Person',
        on_delete=models.PROTECT,
        related_name='person_address_relationships',
        related_query_name='person_address_relationships',
        null=False,
        blank=False,
        db_index=True
    )
    address = models.ForeignKey(
        'Address',
        on_delete=models.PROTECT,
        related_name='person_address_relationships',
        related_query_name='person_address_relationships',
        null=False,
        blank=False,
        db_index=True
    )

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
    rtype = models.ForeignKey(
        'PersonPhoneNumberType',
        on_delete=models.PROTECT,
        related_name='person_phonenumber_relationships',
        related_query_name='person_phonenumber_relationships',
        verbose_name='Person-phonenumber relationship type',
        null=False,
        blank=False,
        db_index=True
    )
    person = models.ForeignKey(
        'Person',
        on_delete=models.PROTECT,
        related_name='person_phonenumber_relationships',
        related_query_name='person_phonenumber_relationships',
        null=False,
        blank=False,
        db_index=True
    )
    phone_number = models.ForeignKey(
        'PhoneNumber',
        on_delete=models.PROTECT,
        related_name='person_phonenumber_relationships',
        related_query_name='person_phonenumber_relationships',
        null=False,
        blank=False,
        db_index=True
    )

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
    rtype = models.ForeignKey(
        'PersonEmailType',
        on_delete=models.PROTECT,
        related_name='person_email_relationships',
        related_query_name='person_email_relationships',
        verbose_name='Person-email relationship type',
        null=False,
        blank=False,
        db_index=True
    )
    person = models.ForeignKey(
        'Person',
        on_delete=models.PROTECT,
        related_name='person_email_relationships',
        related_query_name='person_email_relationships',
        null=False,
        blank=False,
        db_index=True
    )
    email = models.ForeignKey(
        'Email',
        on_delete=models.PROTECT,
        related_name='person_email_relationships',
        related_query_name='person_email_relationships',
        null=False,
        blank=False,
        db_index=True
    )

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
    rtype = models.ForeignKey(
        'CompanyLinkType',
        on_delete=models.PROTECT,
        related_name='company_link_relationships',
        related_query_name='company_link_relationships',
        verbose_name='Company-link relationship type',
        null=False,
        blank=False,
        db_index=True
    )
    company = models.ForeignKey(
        'Company',
        on_delete=models.PROTECT,
        related_name='company_link_relationships',
        related_query_name='company_link_relationships',
        null=False,
        blank=False,
        db_index=True
    )
    link = models.ForeignKey(
        'Link',
        on_delete=models.PROTECT,
        related_name='company_link_relationships',
        related_query_name='company_link_relationships',
        null=False,
        blank=False,
        db_index=True
    )

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
    rtype = models.ForeignKey(
        'CompanyAddressType',
        on_delete=models.PROTECT,
        related_name='company_address_relationships',
        related_query_name='company_address_relationships',
        verbose_name='Company-address relationship type',
        null=False,
        blank=False,
        db_index=True
    )
    company = models.ForeignKey(
        'Company',
        on_delete=models.PROTECT,
        related_name='company_address_relationships',
        related_query_name='company_address_relationships',
        null=False,
        blank=False,
        db_index=True
    )
    address = models.ForeignKey(
        'Address',
        on_delete=models.PROTECT,
        related_name='company_address_relationships',
        related_query_name='company_address_relationships',
        null=False,
        blank=False,
        db_index=True
    )

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
    rtype = models.ForeignKey(
        'CompanyPhoneNumberType',
        on_delete=models.PROTECT,
        related_name='company_phonenumber_relationships',
        related_query_name='company_phonenumber_relationships',
        verbose_name='Company-phonenumber relationship type',
        null=False,
        blank=False,
        db_index=True
    )
    company = models.ForeignKey(
        'Company',
        on_delete=models.PROTECT,
        related_name='company_phonenumber_relationships',
        related_query_name='company_phonenumber_relationships',
        null=False,
        blank=False,
        db_index=True
    )
    phone_number = models.ForeignKey(
        'PhoneNumber',
        on_delete=models.PROTECT,
        related_name='company_phonenumber_relationships',
        related_query_name='company_phonenumber_relationships',
        null=False,
        blank=False,
        db_index=True
    )

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
    rtype = models.ForeignKey(
        'CompanyEmailType',
        on_delete=models.PROTECT,
        related_name='company_email_relationships',
        related_query_name='company_email_relationships',
        verbose_name='Company-email relationship type',
        null=False,
        blank=False,
        db_index=True
    )
    company = models.ForeignKey(
        'Company',
        on_delete=models.PROTECT,
        related_name='company_email_relationships',
        related_query_name='company_email_relationships',
        null=False,
        blank=False,
        db_index=True
    )
    email = models.ForeignKey(
        'Email',
        on_delete=models.PROTECT,
        related_name='company_email_relationships',
        related_query_name='company_email_relationships',
        null=False,
        blank=False,
        db_index=True
    )

    class Meta:
        verbose_name = 'Company-email relationship'
        verbose_name_plural = 'Company-email relationships'

    def __str__(self):
        return f'({self.rtype}, {self.company}, {self.email} [{self.id}])'

# --- End: Company Relationships ---

# --- Start: Entities ---

class Person(Standard):
    given_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    family_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    country = models.ForeignKey(
        'common.Country',
        on_delete=models.PROTECT,
        related_name='persons',
        related_query_name='persons',
        null=True,
        blank=True,
        db_index=True
    )
    state = models.ForeignKey(
        'common.State',
        on_delete=models.PROTECT,
        related_name='persons',
        related_query_name='persons',
        null=True,
        blank=True,
        db_index=True
    )
    notes_md = models.TextField(
        verbose_name='Notes in Markdown', 
        null=True,
        blank=True
    )

    companies = models.ManyToManyField(
        'Company',
        through='PersonCompany',
        through_fields=('person', 'company'),
        related_name='persons',
        related_query_name='persons',
        db_index=True
    )

    emails = models.ManyToManyField(
        'Email',
        through='PersonEmail',
        through_fields=('person', 'email'),
        related_name='persons',
        related_query_name='persons',
        db_index=True
    )

    phone_numbers = models.ManyToManyField(
        'PhoneNumber',
        through='PersonPhoneNumber',
        through_fields=('person', 'phone_number'),
        related_name='persons',
        related_query_name='persons',
        db_index=True
    )

    addresses = models.ManyToManyField(
        'Address',
        through='PersonAddress',
        through_fields=('person', 'address'),
        related_name='persons',
        related_query_name='persons',
        db_index=True
    )

    links = models.ManyToManyField(
        'Link',
        through='PersonLink',
        through_fields=('person', 'link'),
        related_name='persons',
        related_query_name='persons',
        db_index=True
    )

    def __str__(self):
        return f'({self.given_name}, {self.family_name}, {self.country} \
            [{self.id}])'

class Company(Standard):
    company_name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        db_index=True
    )
    company_name_wo_postfix = models.CharField(
        'Company name without postfix',
        max_length=100,
        null=False,
        blank=False,
        db_index=True
    )
    notes_md = models.TextField(
        verbose_name='Notes in Markdown',
        null=True,
        blank=True
    )
    domain = models.CharField(
        max_length=300,
        null=True,
        blank=True,
        db_index=True
    )

    emails = models.ManyToManyField(
        'Email',
        through='CompanyEmail',
        through_fields=('company', 'email'),
        related_name='companies',
        related_query_name='companies',
        db_index=True
    )

    phone_numbers = models.ManyToManyField(
        'PhoneNumber',
        through='CompanyPhoneNumber',
        through_fields=('company', 'phone_number'),
        related_name='companies',
        related_query_name='companies',
        db_index=True
    )

    addresses = models.ManyToManyField(
        'Address',
        through='CompanyAddress',
        through_fields=('company', 'address'),
        related_name='companies',
        related_query_name='companies',
        db_index=True
    )

    links = models.ManyToManyField(
        'Link',
        through='CompanyLink',
        through_fields=('company', 'link'),
        related_name='companies',
        related_query_name='companies',
        db_index=True
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
        max_length=1000,
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
    verified = models.DateTimeField(
        null=True,
        blank=True,
        default=None,
        db_index=True
    )
    link = models.URLField(
        null=False,
        blank=False,
        db_index=True
    )

    def __str__(self):
        return f'({self.link} [{self.id}])'

class Address(Standard):
    address_1 = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        db_index=True
    )
    address_2 = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    address_3 = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    country = models.ForeignKey(
        'common.Country',
        related_name='addresses',
        related_query_name='addresses',
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        db_index=True
    )
    state = models.ForeignKey(
        'common.State',
        related_name='addresses',
        related_query_name='addresses',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    postal_code = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f'({self.address_1}, {self.country} [{self.id}])'

class PhoneNumberType(Choice):
    pass

class PhoneNumber(Standard):
    types = models.ManyToManyField(
        'PhoneNumber',
        related_name='phone_numbers',
        related_query_name='phone_numbers',
        blank=True,
        db_index=True
    )
    country_code = models.PositiveIntegerField(
        null=False,
        blank=False,
        db_index=True
    )
    national_number = models.PositiveIntegerField(
        null=False,
        blank=False,
        db_index=True
    )

    def __str__(self):
        return f'(+{self.country_code} {self.national_number} [{self.id}])'

class BlackListEntry(Standard):
    start = models.DateTimeField(db_index=True)
    invalidated = models.DateTimeField(
        default=None,
        null=True,
        blank=True,
        db_index=True
    )
    reason_md = models.TextField(
        'Reason in Markdown',
        null=True,
        blank=True,
    )

    # At least one of the following must be set
    email = models.ForeignKey(
        'Email',
        related_name='black_list_entries',
        related_query_name='black_list_entries',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    phone_number = models.ForeignKey(
        'PhoneNumber',
        related_name='black_list_entries',
        related_query_name='black_list_entries',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    company = models.ForeignKey(
        'Company',
        related_name='black_list_entries',
        related_query_name='black_list_entries',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    person = models.ForeignKey(
        'Person',
        related_name='black_list_entries',
        related_query_name='black_list_entries',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )

    class Meta:
        verbose_name = 'Blacklist entry'
        verbose_name_plural = 'Blacklist entries'

# --- End: Entities ---