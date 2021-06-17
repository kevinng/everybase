from django.db import models
from common.models import Standard, Choice
import random
from hashid_field import HashidAutoField

class PaymentLink(Standard):
    """Payment link sent to user.

    Last updated: 11 May 2021, 6:01 PM
    """

    id = HashidAutoField(primary_key=True)
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
    currency = models.ForeignKey(
        'Currency',
        null=True,
        blank=True,
        related_name='payment_links',
        related_query_name='payment_links',
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

    Last updated: 27 April 2021, 9:03 PM
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
    payment_link = models.ForeignKey(
        'PaymentLink',
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