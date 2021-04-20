from django.db import models
from common.models import (Standard, Choice, LowerCaseCharField,
    LowerCaseEmailField)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import random

class PhoneNumberType(Choice):
    pass

def validate_phone_number_country_code(value):
    if value is not None and len(value) > 0 and value.startswith('+'):
        raise ValidationError(
            _('%(value)s must not start with "+"'),
            params={'value': value},
        )

class PhoneNumber(Standard):
    types = models.ManyToManyField(
        'PhoneNumberType',
        related_name='phone_numbers',
        related_query_name='phone_numbers',
        blank=True,
        db_index=True
    )
    country_code = models.CharField(
        max_length=50,
        default=None,
        null=False,
        blank=False,
        db_index=True,
        validators=[validate_phone_number_country_code]
    )
    national_number = models.CharField(
        max_length=100,
        default=None,
        null=False,
        blank=False,
        db_index=True
    )

    def __str__(self):
        return f'(+{self.country_code} {self.national_number} [{self.id}])'

    class Meta:
        unique_together = (('country_code', 'national_number'), )

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

_USER_KEY_LENGTH = 16
def get_user_key(length=_USER_KEY_LENGTH):
    """Generates and returns a URL friendly key.

    Parameters
    ----------
    length : int
        The length of the key to generate

    Returns
    -------
    key
        URL friendly key
    """
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890'
    key = ''
    for i in range(0, length):
        p = random.randint(0, len(chars)-1)
        key += chars[p]
    return key

class User(Standard):
    key = models.CharField(
        max_length=_USER_KEY_LENGTH,
        unique=True,
        default=get_user_key,
        db_index=True
    )
    phone_number = models.OneToOneField(
        'PhoneNumber',
        related_name='users',
        related_query_name='users',
        on_delete=models.PROTECT,
        db_index=True
    )

    name = models.CharField(
        max_length=100,
        db_index=True
    )

    email = models.ForeignKey(
        'Email',
        related_name='users',
        related_query_name='users',
        on_delete=models.PROTECT,
        db_index=True
    )

    def __str__(self):
        return f'({self.name} [{self.id}])'

class AccessedURL(Standard):
    user = models.ForeignKey(
        'User',
        related_name='accessed_urls',
        related_query_name='accessed_urls',
        on_delete=models.PROTECT,
        db_index=True
    )
    first_accessed = models.DateTimeField(db_index=True)
    last_accessed = models.DateTimeField(db_index=True)
    count = models.IntegerField(db_index=True)
    url = models.URLField(
        'URL',
        unique=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Accessed URL'
        verbose_name_plural = 'Accessed URLs'
    
    def __str__(self):
        return f'({self.url} [{self.id}])'

class UserIPDevice(Standard):
    user = models.ForeignKey(
        'User',
        related_name='ip_devices',
        related_query_name='ip_devices',
        on_delete=models.PROTECT,
        db_index=True
    )
    first_accessed = models.DateTimeField(db_index=True)
    last_accessed = models.DateTimeField(db_index=True)
    count = models.IntegerField(db_index=True)
        
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        db_index=True
    )
    is_mobile = models.BooleanField(
        null=True,
        blank=True,
        db_index=True
    )
    is_tablet = models.BooleanField(
        null=True,
        blank=True,
        db_index=True
    )
    is_touch_capable = models.BooleanField(
        null=True,
        blank=True,
        db_index=True
    )
    is_pc = models.BooleanField(
        null=True,
        blank=True,
        db_index=True
    )
    is_bot = models.BooleanField(
        null=True,
        blank=True,
        db_index=True
    )
    browser = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    browser_family = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    browser_version = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    browser_version_string = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    os = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    os_version = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    os_version_string = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    device = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    device_family = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
        
    accessed_urls = models.ManyToManyField(
        'AccessedURL',
        related_name='user_ip_devices',
        related_query_name='user_ip_devices',
        db_index=True
    )

    class Meta:
        verbose_name = 'User IP-Device'
        verbose_name_plural = 'User IP-Devices'

class ProductType(Standard, Choice):
    pass

class CompanyProductType(Standard):
    popularity = models.FloatField(db_index=True)

    company = models.ForeignKey(
        'Company',
        on_delete=models.PROTECT,
        db_index=True
    )
    product_type = models.ForeignKey(
        'ProductType',
        on_delete=models.PROTECT,
        db_index=True
    )

class Company(Standard):
    display_name = models.CharField(
        max_length=200,
        db_index=True
    )
    notes = models.TextField(db_index=True)

    product_types = models.ManyToManyField(
        'ProductType',
        through='CompanyProductType',
        related_name='companies',
        related_query_name='companies',
        db_index=True
    )

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return f'({self.display_name} [{self.id}])'

class CompanyProduct(Standard):
    popularity = models.FloatField(db_index=True)

    company = models.ForeignKey(
        'Company',
        related_name='companies',
        related_query_name='companies',
        on_delete=models.PROTECT,
        db_index=True
    )
    product = models.ForeignKey(
        'Product',
        related_name='products',
        related_query_name='products',
        on_delete=models.PROTECT,
        db_index=True
    )

class Product(Standard):
    display_name = models.CharField(
        max_length=200,
        db_index=True
    )
    notes = models.TextField(db_index=True)
    
    product_type = models.ForeignKey(
        'ProductType',
        related_name='products',
        related_query_name='products',
        on_delete=models.PROTECT,
        db_index=True
    )

    def __str__(self):
        return f'({self.display_name} [{self.id}])'