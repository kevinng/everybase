from django.db import models
from common.models import (Standard, Choice, LowerCaseCharField,
    LowerCaseEmailField)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import random

class PhoneNumberType(Choice):
    """Phone number type.

    Last updated: 21 April 2021, 11:23 PM
    """
    pass

def validate_country_code(value):
    """Validates country code. Raise ValidationError if value is invalid.

    Parameters
    ----------
    value : str
        Phone number's country code
    """

    if value is not None and len(value) > 0 and (value.startswith('+') or \
        not value.isnumeric()):
        raise ValidationError(
            _('%(value)s must be numeric and not start with "+"'),
            params={'value': value},
        )

def validate_national_number(value):
    """Validates national number. Raise ValidationError if value is invalid.

    Parameters
    ----------
    value : str
        Phone number's national number
    """

    if value is not None and len(value) > 0 and not value.isnumeric():
        raise ValidationError(
            _('%(value)s must be numeric'), params={'value': value},
        )

class PhoneNumber(Standard):
    """Phone numbers.
    
    Last updated: 27 April 2021, 11:43 AM
    """

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
        db_index=True,
        validators=[validate_country_code]
    )
    national_number = models.CharField(
        max_length=100,
        default=None,
        db_index=True,
        validators=[validate_national_number]
    )

    def __str__(self):
        return f'(+{self.country_code} {self.national_number} [{self.id}])'

    class Meta:
        unique_together = ['country_code', 'national_number']

class Email(Standard):
    """Email.

    Last updated: 21 April 2021, 11:15 PM
    """

    email = LowerCaseEmailField(
        unique=True,
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
    """Invalid email.

    Last updated: 21 April 2021, 11:13 PM
    """

    email = LowerCaseCharField(
        max_length=1000,
        unique=True,
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
    """User details.

    Last updated: 28 April 2021, 3:35 PM
    """

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
    is_banned = models.BooleanField(
        default=False,
        db_index=True
    )
    notes = models.TextField(
        null=True,
        blank=True
    )

    email = models.OneToOneField(
        'Email',
        related_name='user',
        related_query_name='user',
        on_delete=models.PROTECT,
        db_index=True
    )

    def __str__(self):
        return f'({self.name} [{self.id}])'

class AccessedURL(Standard):
    """Accessed URL.

    Last updated: 21 April 2021, 10:57 PM
    """

    user = models.ForeignKey(
        'User',
        related_name='accessed_urls',
        related_query_name='accessed_urls',
        on_delete=models.PROTECT,
        db_index=True
    )
    first_accessed = models.DateTimeField(db_index=True)
    last_accessed = models.DateTimeField(db_index=True)
    url = models.URLField(
        'URL',
        db_index=True
    )
    count = models.IntegerField(db_index=True)

    class Meta:
        verbose_name = 'Accessed URL'
        verbose_name_plural = 'Accessed URLs'
        unique_together = ['user', 'url']
        index_together = ['user', 'url']
    
    def __str__(self):
        return f'({self.url} [{self.id}])'

class UserIPDevice(Standard):
    """IP address and device user used to access our system.

    Last updated: 21 April 2021, 10:56 PM
    """

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
    """Product type.

    Last updated: 21 April 2021, 10:45 PM
    """
    pass

class Company(Standard, Choice):
    """Company selling products. Not companies of users.

    Last updated: 5 May 2021, 2:53 PM
    """

    url = models.URLField(
        null=True,
        blank=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

class CompanyProduct(Standard):
    """Relationship between company and product.

    Last updated: 27 April 2021, 1:20 PM
    """

    popularity = models.FloatField(
        null=True,
        blank=True,
        db_index=True
    )

    company = models.ForeignKey(
        'Company',
        related_name='company_products',
        related_query_name='company_products',
        on_delete=models.PROTECT,
        db_index=True
    )
    product = models.ForeignKey(
        'Product',
        related_name='company_products',
        related_query_name='company_products',
        on_delete=models.PROTECT,
        db_index=True
    )

    def __str__(self):
        return f'({self.company.name}, {self.product.name} \
            [{self.id}])'

class CompanyProductType(Standard):
    """Relationship between company and product type.

    Last updated: 27 April 2021, 1:11 PM
    """

    popularity = models.FloatField(
        null=True,
        blank=True,
        db_index=True
    )

    company = models.ForeignKey(
        'Company',
        related_name='company_product_types',
        related_query_name='company_product_types',
        on_delete=models.PROTECT,
        db_index=True
    )
    product_type = models.ForeignKey(
        'ProductType',
        related_name='company_product_types',
        related_query_name='company_product_types',
        on_delete=models.PROTECT,
        db_index=True
    )

    def __str__(self):
        return f'({self.company.name}, {self.product_type.name} \
            [{self.id}])'

class Product(Standard, Choice):
    """Product.

    Last updated: 6 May 2021, 1:35 PM
    """
    
    url = models.URLField(
        'URL',
        db_index=True
    )
    product_type = models.ForeignKey(
        'ProductType',
        related_name='products',
        related_query_name='products',
        on_delete=models.PROTECT,
        db_index=True
    )

class ProductSpecificationType(Standard, Choice):
    """Specification type of a product. E.g., 501K of nitrile gloves. Note: this
    is a 'type'. Whether a nitrile gloves supply has 501K or not - is defined in
    ProductSpecification.

    Last updated: 6 May 2021, 1:34 PM
    """
	
    product_type = models.ForeignKey(
        'ProductType',
        related_name='product_specifications',
        related_query_name='product_specifications',
        on_delete=models.PROTECT,
        db_index=True
    )

class ProductSpecification(Standard):
    """Details on specification existance or value of a
    product-specification-type on a product.

    Last updated: 21 April 2021, 9:09 PM
    """

    is_exists = models.BooleanField(
        null=True,
        blank=True,
        db_index=True
    )
    float_value = models.FloatField(
        null=True,
        blank=True,
        db_index=True
    )
    string_value = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    
    product_specification_type = models.ForeignKey(
        'ProductSpecificationType',
        related_name='product_specifications',
        related_query_name='product_specifications',
        on_delete=models.PROTECT,
        db_index=True
    )

    # At least 1 of the following must be set
    product = models.ForeignKey(
        'Product',
        related_name='product_specifications',
        related_query_name='product_specifications',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    # supply = models.ForeignKey(
    #     'Supply',
    #     related_name='product_specifications',
    #     related_query_name='product_specifications',
    #     null=True,
    #     blank=True,
    #     on_delete=models.PROTECT,
    #     db_index=True
    # )
    # demand = models.ForeignKey(
    #     'Demand',
    #     related_name='product_specifications',
    #     related_query_name='product_specifications',
    #     null=True,
    #     blank=True,
    #     on_delete=models.PROTECT,
    #     db_index=True
    # )

    # def __str__(self):
    #     return f'({self.product_specification_type.name}, \
    #         {self.product.name}, {self.is_exists}, {self.string_value}, \
    #         {self.float_value}, [{self.id}])'

    # def clean(self):
    #     super(ProductSpecification, self).clean()

    #     if self.product is None and self.supply is None and self.demand:
    #         raise ValidationError('Either product, supply, demand must be set.')

class IncotermAvailability(Standard, Choice):
    """Incoterm/availability - e.g., FOB, CIF, OTG, pre-order.

    Last updated: 21 April 2021, 4:34 PM
    """
    class Meta:
        verbose_name = 'Incoterm/Availability'
        verbose_name_plural = 'Incoterms/Availabilities'

class Location(Standard, Choice):
    """Location.

    Last updated: 21 April 2021, 3:24 PM
    """
    parent = models.ForeignKey(
        'Location',
        null=True,
        blank=True,
        related_name='children',
        related_query_name='children',
        on_delete=models.PROTECT,
        db_index=True
    )

class PaymentTerm(Standard, Choice):
    """Payment term.

    Last updated: 21 April 2021, 3:21 PM
    """
    
    # At least one of the following must be set.
    # supply_quote = models.ForeignKey(
    #     'SupplyQuote',
    #     null=True,
    #     blank=True,
    #     related_name='payment_terms',
    #     related_query_name='payment_terms',
    #     on_delete=models.PROTECT,
    #     db_index=True
    # )
    # demand_quote = models.ForeignKey(
    #     'DemandQuote',
    #     null=True,
    #     blank=True,
    #     related_name='payment_terms',
    #     related_query_name='payment_terms',
    #     on_delete=models.PROTECT,
    #     db_index=True
    # )

    # def clean(self):
    #     super(PaymentTerm, self).clean()

    #     # Either supply_quote or demand_quote must be set.
    #     if (self.supply_quote is None and self.demand_quote is None) or \
    #         (self.supply_quote is not None and self.demand_quote is not None):
    #         raise ValidationError('Either supply_quote or demand_quote must be \
    #             set.')

class Packing(Standard):
    """Packing.

    Last updated: 21 April 2021, 3:08 PM
    """

    base_quantity = models.FloatField(db_index=True)
    base_uom = models.ForeignKey(
        'UnitOfMeasure',
        related_name='packing_base_uoms',
        related_query_name='packing_base_uoms',
        on_delete=models.PROTECT,
        db_index=True
    )
    pack_uom = models.ForeignKey(
        'UnitOfMeasure',
        related_name='packing_pack_uom',
        related_query_name='packing_pack_uom',
        on_delete=models.PROTECT,
        db_index=True
    )

    # At least one of the following must be set.
    # supply_quote = models.ForeignKey(
    #     'SupplyQuote',
    #     null=True,
    #     blank=True,
    #     related_name='packings',
    #     related_query_name='packings',
    #     on_delete=models.PROTECT,
    #     db_index=True
    # )
    # demand_quote = models.ForeignKey(
    #     'DemandQuote',
    #     null=True,
    #     blank=True,
    #     related_name='packings',
    #     related_query_name='packings',
    #     on_delete=models.PROTECT,
    #     db_index=True
    # )

    # def clean(self):
    #     super(Packing, self).clean()

    #     # Either supply_quote or demand_quote must be set.
    #     if (self.supply_quote is None and self.demand_quote is None) or \
    #         (self.supply_quote is not None and self.demand_quote is not None):
    #         raise ValidationError('Either supply_quote or demand_quote must be \
    #             set.')

    def __str__(self):
        return f'({self.base_quantity} {self.base_uom} in 1 {self.pack_uom} [{self.id}])'

class UnitOfMeasure(Standard, Choice):
    """Unit of measure.

    Last updated: 21 April 2021, 2:44 PM
    """

    plural_name = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )

    product_type = models.ForeignKey(
        'ProductType',
        related_name='unit_of_measures',
        related_query_name='unit_of_measures',
        on_delete=models.PROTECT,
        db_index=True
    )