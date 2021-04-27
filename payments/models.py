from django.db import models
from common.models import Standard, Choice

class StripeSession(Standard):
    """Stripe session.

    Last updated: 25 April 2021, 4:12 PM
    """

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
    currency = models.ForeignKey(
        'Currency',
        null=True,
        blank=True,
        related_name='stripe_sessions',
        related_query_name='stripe_sessions',
        on_delete=models.PROTECT,
        db_index=True
    )
    unit_amount = models.FloatField(
        null=True,
        blank=True,
        db_index=True
    )

class PaymentEvent(Standard):
    """Payment event.

    Last updated: 25 April 2021, 3:45 PM
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
    match = models.ForeignKey(
        'relationships.Match',
        related_name='payment_events',
        related_query_name='payment_events',
        on_delete=models.PROTECT,
        db_index=True
    )
    session = models.ForeignKey(
        'StripeSession',
        related_name='payment_events',
        related_query_name='payment_events',
        on_delete=models.PROTECT,
        db_index=True
    )

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