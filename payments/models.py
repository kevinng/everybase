from locale import currency
from django.db import models
from common.models import Standard, Choice

class Currency(Choice):
    class Meta:
        verbose_name = 'Currencies'
        verbose_name_plural = 'Currencies'

class StripeCallbackSession(Standard):
    """Stripe session object details recorded on callback

    Updated: 2 March 2022, 9:20 PM
    """
    session_id = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        db_index=True
    )
    amount_total = models.IntegerField(
        blank=True,
        null=True,
        db_index=True
    )
    currency = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        db_index=True
    )
    customer = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        db_index=True
    )
    customer_details_email = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        db_index=True
    )
    mode = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        db_index=True
    )
    payment_intent = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        db_index=True
    )
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('paid', 'Paid'),
            ('unpaid', 'Unpaid'),
            ('no_payment_required', 'No Payment Required')
        ],
        blank=True,
        null=True,
        db_index=True
    )
    success_url = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        db_index=True
    )
    cancel_url = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        db_index=True
    )

class StripeCheckoutSession(Standard):
    """Stripe session object details recorded on checkout

    Updated: 2 March 2022, 9:20 PM
    """
    customer = models.ForeignKey(
        'StripeCustomer',
        related_name='checkout_sessions',
        related_query_name='checkout_sessions',
        on_delete=models.PROTECT,
        db_index=True  
    )
    session_id = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        db_index=True
    )
    mode = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        db_index=True
    )
    success_url = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        db_index=True
    )
    cancel_url = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        db_index=True
    )

class StripePrice(Standard):
    """Stripe price

    Updated: 2 March 2022, 9:20 PM
    """
    api_id = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        db_index=True
    )
    name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        db_index=True
    )
    description = models.TextField(
        blank=True,
        null=True
    )
    currency = models.ForeignKey(
        'Currency',
        related_name='stripe_prices',
        related_query_name='stripe_prices',
        on_delete=models.PROTECT,
        db_index=True
    )
    value = models.FloatField(
        blank=True,
        null=True,
        db_index=True
    )

class StripeCustomer(Standard):
    """Customer in Stripe

    Updated: 15 March 2022, 10:24 PM
    """
    user = models.OneToOneField(
        'relationships.User',
        on_delete=models.PROTECT,
        unique=True,
        db_index=True
    )
    api_id = models.CharField(
        max_length=200,
        db_index=True
    )

class StripeCheckoutSessionLineItem(Standard):
    """Line item in Stripe session recorded on checkout

    Updated: 2 March 2022, 9:20 PM
    """
    session = models.ForeignKey(
        'StripeCheckoutSession',
        related_name='line_items',
        related_query_name='line_items',
        on_delete=models.PROTECT,
        db_index=True
    )
    price = models.ForeignKey(
        'StripePrice',
        related_name='line_items',
        related_query_name='line_items',
        on_delete=models.PROTECT,
        db_index=True
    )
    
    quantity = models.IntegerField(
        db_index=True
    )

class CreditsEvent(Standard):
    """Credits event for a user. E.g., credit top-up as a result of buying a credits pack.

    Updated: 2 March 2022, 9:20 PM
    """
    user = models.ForeignKey(
        'relationships.User',
        related_name='credits_events',
        related_query_name='credits_events',
        on_delete=models.PROTECT,
        db_index=True
    )
    value = models.IntegerField(
        blank=True,
        null=True,
        db_index=True
    )
    type = models.CharField(
        max_length=20,
        choices=[
            ('top-up', 'Top-Up'),
            ('use', 'Use'),
            ('admin', 'Admin')
        ],
        db_index=True
    )
    session = models.ForeignKey(
        'StripeCallbackSession',
        related_name='credits_events',
        related_query_name='credits_events',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    notes = models.TextField(
        blank=True,
        null=True
    )