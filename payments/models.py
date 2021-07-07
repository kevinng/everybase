from django.db import models
from common.models import Standard, Choice
from hashid_field import HashidAutoField

class PaymentHash(Standard):
    """Hash of payment link sent to user.

    Last updated: 18 June 2021, 10:17
    """

    id = HashidAutoField(primary_key=True)
    expired = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )

    user = models.ForeignKey(
        'relationships.User',
        related_name='payment_links',
        related_query_name='payment_links',
        on_delete=models.PROTECT,
        db_index=True
    )
    match = models.ForeignKey(
        'relationships.Match',
        null=True,
        blank=True,
        related_name='payment_links',
        related_query_name='payment_links',
        on_delete=models.PROTECT,
        db_index=True
    )
    
    started = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    succeeded = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    failed = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    session_id = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True        
    )
    
    product_name = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    currency = models.ForeignKey(
        'Currency',
        null=True,
        blank=True,
        related_name='payment_hashes',
        related_query_name='payment_hashes',
        on_delete=models.PROTECT,
        db_index=True
    )
    unit_amount = models.FloatField(
        null=True,
        blank=True,
        db_index=True
    )

    def __str__(self):
        return f'({self.session_id}, {self.unit_amount}, {self.currency} \
            [{self.id}])'

class PaymentEvent(Standard):
    """Payment event.

    Last updated: 17 June 2021, 5:55 PM
    """

    event_type = models.ForeignKey(
        'PaymentEventType',
        related_name='payment_events',
        related_query_name='payment_events',
        on_delete=models.PROTECT,
        db_index=True
    )
    currency = models.ForeignKey(
        'Currency',
        related_name='payment_events',
        related_query_name='payment_events',
        on_delete=models.PROTECT,
        db_index=True
    )	
    amount = models.FloatField(db_index=True)
	
    user = models.ForeignKey(
        'relationships.User',
        related_name='payment_events',
        related_query_name='payment_events',
        on_delete=models.PROTECT,
        db_index=True
    )
    payment_hash = models.ForeignKey(
        'PaymentHash',
        related_name='payment_events',
        related_query_name='payment_events',
        on_delete=models.PROTECT,
        db_index=True
    )

    def __str__(self):
        return f'({self.user}, {self.amount}, {self.currency} \
            [{self.id}])'

class PaymentEventType(Choice):
    """Payment event type.

    Last updated: 25 April 2021, 4:11 PM
    """
    pass

class Currency(Choice):
    """Currency. E.g., USD.

    Last updated: 23 April 2021, 6:52 PM
    """

    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'

PAYMENT_LINK_ACCESS_SUCCESSFUL = 'PAYMENT_LINK_ACCESS_SUCCESSFUL'
PAYMENT_LINK_ACCESS_FAILED = 'PAYMENT_LINK_ACCESS_FAILED'
class PaymentLinkAccess(Standard):
    """A single access of a payment hash/URL.

    Last updated: 18 June 2021, 2:35 PM
    """
    accessed = models.DateTimeField(
        db_index=True,
        auto_now=True
    )
    outcome = models.CharField(
        max_length=200,
        choices=[
            (PAYMENT_LINK_ACCESS_SUCCESSFUL, PAYMENT_LINK_ACCESS_SUCCESSFUL),
            (PAYMENT_LINK_ACCESS_FAILED, PAYMENT_LINK_ACCESS_FAILED),
        ],
        null=True,
        blank=True,
        db_index=True
    )
        
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
    os_family = models.CharField(
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
        
    hash = models.ForeignKey(
        'PaymentHash',
        related_name='accesses',
        related_query_name='accesses',
        on_delete=models.PROTECT,
        db_index=True
    )

    class Meta:
        verbose_name = 'Phone hash access'
        verbose_name_plural = 'Phone hash accesses'