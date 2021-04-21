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
    """User details.

    Last updated: 21 April 2021, 11:10 PM
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
        blank=True,
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

class CompanyProductType(Standard):
    """Relationship between company and product type.

    Last updated: 21 April 2021, 10:29 PM
    """

    popularity = models.FloatField(
        null=True,
        blank=True,
        db_index=True
    )

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

    def __str__(self):
        return f'({self.company.display_name}, {self.product_type.name} \
            [{self.id}])'

class Company(Standard):
    """Company selling products. Not companies of users.

    Last updated: 21 April 2021, 10:24 PM
    """

    display_name = models.CharField(
        max_length=200,
        db_index=True
    )
    notes = models.TextField(
        null=True,
        blank=True,
        db_index=True
    )

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
    """Relationship between company and product.

    Last updated: 21 April 2021, 9:51 PM
    """

    popularity = models.FloatField(
        null=True,
        blank=True,
        db_index=True
    )

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

    def __str__(self):
        return f'({self.company.display_name}, {self.product.display_name} \
            [{self.id}])'

class Product(Standard):
    """Product.

    Last updated: 21 April 2021, 9:46 PM
    """

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

class ProductSpecificationType(Standard):
    """Specification type of a product. E.g., 501K of nitrile gloves. Note: this
    is a 'type'. Whether a nitrile gloves supply has 501K or not - is defined in
    ProductSpecification.

    Last updated: 21 April 2021, 9:33 PM
    """

    display_name = models.CharField(
        max_length=200,
        db_index=True
    )
    notes = models.TextField(
        null=True,
        blank=True,
        db_index=True
    )
	
    product_type = models.ForeignKey(
        'ProductType',
        related_name='product_specifications',
        related_query_name='product_specifications',
        on_delete=models.PROTECT,
        db_index=True
    )

    def __str__(self):
        return f'({self.display_name} [{self.id}])'

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
    value = models.FloatField(
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
    supply = models.ForeignKey(
        'Supply',
        related_name='product_specifications',
        related_query_name='product_specifications',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    demand = models.ForeignKey(
        'Demand',
        related_name='product_specifications',
        related_query_name='product_specifications',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )

    def __str__(self):
        return f'({self.product_specification_type.display_name}, \
            {self.product.display_name}, {self.is_exists}, {self.value}, \
            [{self.id}])'

    def clean(self):
        super(ProductSpecification, self).clean()

        # Either supply_quote or demand_quote must be set.
        if self.product is None and self.supply is None and self.demand:
            raise ValidationError('Either product, supply, demand must be set.')

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
    pass

class PaymentTerm(Standard, Choice):
    """Payment term.

    Last updated: 21 April 2021, 3:21 PM
    """
    
    # At least one of the following must be set.
    supply_quote = models.ForeignKey(
        'SupplyQuote',
        null=True,
        blank=True,
        related_name='payment_terms',
        related_query_name='payment_terms',
        on_delete=models.PROTECT,
        db_index=True
    )
    demand_quote = models.ForeignKey(
        'DemandQuote',
        null=True,
        blank=True,
        related_name='payment_terms',
        related_query_name='payment_terms',
        on_delete=models.PROTECT,
        db_index=True
    )

    def clean(self):
        super(PaymentTerm, self).clean()

        # Either supply_quote or demand_quote must be set.
        if (self.supply_quote is None and self.demand_quote is None) or \
            (self.supply_quote is not None and self.demand_quote is not None):
            raise ValidationError('Either supply_quote or demand_quote must be \
                set.')

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
    supply_quote = models.ForeignKey(
        'SupplyQuote',
        null=True,
        blank=True,
        related_name='packings',
        related_query_name='packings',
        on_delete=models.PROTECT,
        db_index=True
    )
    demand_quote = models.ForeignKey(
        'DemandQuote',
        null=True,
        blank=True,
        related_name='packings',
        related_query_name='packings',
        on_delete=models.PROTECT,
        db_index=True
    )

    def clean(self):
        super(Packing, self).clean()

        # Either supply_quote or demand_quote must be set.
        if (self.supply_quote is None and self.demand_quote is None) or \
            (self.supply_quote is not None and self.demand_quote is not None):
            raise ValidationError('Either supply_quote or demand_quote must be \
                set.')

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

class ExcludedPrice(Standard, Choice):
    """Prices excluded from quoted price - e.g., VAT, GST.

    Last updated: 21 April 2021, 2:45 PM
    """

    # At least one of the following must be set.
    supply_quote = models.ForeignKey(
        'SupplyQuote',
        null=True,
        blank=True,
        related_name='excluded_prices',
        related_query_name='excluded_prices',
        on_delete=models.PROTECT,
        db_index=True
    )
    demand_quote = models.ForeignKey(
        'DemandQuote',
        null=True,
        blank=True,
        related_name='excluded_prices',
        related_query_name='excluded_prices',
        on_delete=models.PROTECT,
        db_index=True
    )

    def clean(self):
        super(ExcludedPrice, self).clean()

        # Either supply_quote or demand_quote must be set.
        if (self.supply_quote is None and self.demand_quote is None) or \
            (self.supply_quote is not None and self.demand_quote is not None):
            raise ValidationError('Either supply_quote or demand_quote must be \
                set.')

class Lead(Standard):
    """Abstract lead to be overriden by Supply and Demand.

    Last updated: 21 April 2021, 10:01 PM
    """

    product_type = models.ForeignKey(
        'ProductType',
        related_name='%(class)s_leads',
        related_query_name='%(class)s_leads',
        on_delete=models.PROTECT,
        db_index=True
    )
    company = models.ForeignKey(
        'Company',
        null=True,
        blank=True,
        related_name='%(class)s_leads',
        related_query_name='%(class)s_leads',
        on_delete=models.PROTECT,
        db_index=True
    )
    product = models.ForeignKey(
        'Product',
        null=True,
        blank=True,
        related_name='%(class)s_leads',
        related_query_name='%(class)s_leads',
        on_delete=models.PROTECT,
        db_index=True
    )

    user = models.ForeignKey(
        'User',
        related_name='%(class)s_leads',
        related_query_name='%(class)s_leads',
        on_delete=models.PROTECT,
        db_index=True
    )
    
    def __str__(self):
        return f'({self.product_type.name}, {self.user.name} [{self.id}])'
    
    class Meta:
        abstract = True

class Supply(Lead):
    """Supply.

    Last updated: 21 April 2021, 8:30 PM
    """

    class Meta:
        verbose_name = 'Supply'
        verbose_name_plural = 'Supplies'

class Demand(Lead):
    """Demand.

    Last updated: 21 April 2021, 8:30 PM
    """

    pass

class LeadQuote(Standard):
    """Abstract lead quote class - to be extended by SupplyQuote and
    DemandQuote.

    Last updated: 21 April 2021, 10:06 PM
    """

    entered = models.DateTimeField(
        db_index=True
    )

    price = models.FloatField(
        null=True,
        blank=True,
        db_index=True
    )
    price_uom = models.ForeignKey(
        'UnitOfMeasure',
        null=True,
        blank=True,
        related_name='%(class)s_price_uoms',
        related_query_name='%(class)s_price_uoms',
        on_delete=models.PROTECT,
        db_index=True
    )
    currency = models.ForeignKey(
        'payments.Currency',
        null=True,
        blank=True,
        related_name='%(class)s_currencies',
        related_query_name='%(class)s_currencies',
        on_delete=models.PROTECT,
        db_index=True
    )

    incoterm_availability = models.ForeignKey(
        'IncotermAvailability',
        null=True,
        blank=True,
        related_name='%(class)s_incoterm_availabilities',
        related_query_name='%(class)s_incoterm_availabilities',
        on_delete=models.PROTECT,
        db_index=True
    )
    location = models.ForeignKey(
        'Location',
        null=True,
        blank=True,
        related_name='%(class)s_locations',
        related_query_name='%(class)s_locations',
        on_delete=models.PROTECT,
        db_index=True
    )

    total_quantity = models.FloatField(
        null=True,
        blank=True,
        db_index=True
    )
    total_quantity_uom = models.ForeignKey(
        'UnitOfMeasure',
        null=True,
        blank=True,
        related_name='%(class)s_total_quantity_uoms',
        related_query_name='%(class)s_total_quantity_uoms',
        on_delete=models.PROTECT,
        db_index=True
    )

    moq_quantity = models.FloatField(
        null=True,
        blank=True,
        db_index=True
    )
    moq_quantity_uom = models.ForeignKey(
        'UnitOfMeasure',
        null=True,
        blank=True,
        related_name='%(class)s_moq_quantity_uoms',
        related_query_name='%(class)s_moq_quantity_uoms',
        on_delete=models.PROTECT,
        db_index=True
    )

    delivery_interval_quantity = models.FloatField(
        null=True,
        blank=True,
        db_index=True
    )
    delivery_interval_quantity_uom = models.ForeignKey(
        'UnitOfMeasure',
        null=True,
        blank=True,
        related_name='%(class)s_delivery_interval_quantity_uoms',
        related_query_name=\
            '%(class)s_delivery_interval_quantity_uoms',
        on_delete=models.PROTECT,
        db_index=True
    )
    delivery_interval_count = models.IntegerField(
        null=True,
        blank=True,
        db_index=True
    )
    delivery_interval_length = models.IntegerField(
        null=True,
        blank=True,
        db_index=True
    )
    delivery_interval_uom = models.CharField(
        max_length=2,
        null=True,
        blank=True,
        choices=[
            ('d', 'Day'),
            ('w', 'Week'),
            ('m', 'Month'),
            ('y', 'Year')
        ],
        db_index=True
    )

    commission_percentage_sales = models.FloatField(
        null=True,
        blank=True,
        db_index=True
    )
    commission_amount = models.FloatField(
        null=True,
        blank=True,
        db_index=True
    )
    commission_amount_currency = models.ForeignKey(
        'payments.Currency',
        null=True,
        blank=True,
        related_name='%(class)s_commission_amount_currencies',
        related_query_name='%(class)s_commission_amount_currencies',
        on_delete=models.PROTECT,
        db_index=True
    )
    commission_amount_uom = models.ForeignKey(
        'UnitOfMeasure',
        null=True,
        blank=True,
        related_name='%(class)s_commission_amount_uom',
        related_query_name='%(class)s_commission_amount_uom',
        on_delete=models.PROTECT,
        db_index=True
    )

    class Meta:
        abstract = True

class SupplyQuote(LeadQuote):
    """Supply quote.

    Last updated: 21 April 2021, 5:23 PM
    """

    supply = models.ForeignKey(
        'Supply',
        related_name='supply_quotes',
        related_query_name='supply_quotes',
        on_delete=models.PROTECT,
        db_index=True
    )

    def __str__(self):
        return f'({self.supply.product_type.name}, [{self.id}])'

class DemandQuote(LeadQuote):
    """Demand quote.

    Last updated: 21 April 2021, 5:23 PM
    """

    demand = models.ForeignKey(
        'Demand',
        related_name='demand_quotes',
        related_query_name='demand_quotes',
        on_delete=models.PROTECT,
        db_index=True
    )

    def __str__(self):
        return f'({self.demand.product_type.name}, [{self.id}])'