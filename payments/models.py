import uuid
from django.db import models
from common.models import Standard, Choice

# General

class Currency(Choice):
    class Meta:
        verbose_name = 'Currencies'
        verbose_name_plural = 'Currencies'

# Stripe

class StripePrice(Standard):
    """Stripe price

    Updated: 12 September 2022, 9:17 PM
    """
    price_id = models.CharField(
        max_length=200,
        db_index=True
    )
    name = models.CharField(
        max_length=200,
        db_index=True
    )
    currency = models.ForeignKey(
        'Currency',
        related_name='stripe_prices',
        related_query_name='stripe_prices',
        on_delete=models.PROTECT,
        db_index=True
    )
    value = models.FloatField(
        db_index=True
    )

class StripeEvent(Standard):
    """Stripe Event object fields recorded in a callback.

    Updated: 12 September 2022, 9:24 PM
    """
    event_id = models.CharField(
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

class StripeCustomer(Standard):
    """Customer in Stripe

    Updated: 12 September 2022, 9:17 PM
    """
    user = models.OneToOneField(
        'relationships.User',
        on_delete=models.PROTECT,
        unique=True,
        db_index=True
    )
    customer_id = models.CharField(
        default=uuid.uuid4,
        unique=True,
        max_length=200,
        db_index=True
    )

class StripeCheckoutSession(Standard):
    """Stripe session object details recorded on checkout.

    Updated: 12 September 2022, 10:00 PM
    """
    contact_user_credits_bundle = models.ForeignKey(
        'ContactUserCreditsBundle',
        related_name='stripe_checkout_sessions',
        related_query_name='stripe_checkout_sessions',
        on_delete=models.PROTECT,
        db_index=True
    )
    alert_notification_credits_bundle = models.ForeignKey(
        'AlertNotificationCreditsBundle',
        related_name='stripe_checkout_sessions',
        related_query_name='stripe_checkout_sessions',
        on_delete=models.PROTECT,
        db_index=True
    )
    subscription_plan = models.ForeignKey(
        'SubscriptionPlan',
        related_name='stripe_checkout_sessions',
        related_query_name='stripe_checkout_sessions',
        on_delete=models.PROTECT,
        db_index=True
    )
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

class StripeCheckoutSessionLineItem(Standard):
    """Line item in Stripe session recorded on checkout.

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

# Business Model

class SubscriptionPlan(Standard):
    """Subscription plan.

    Updated: 12 September 2022, 10:27 PM
    """
    name = models.CharField(
        max_length=200,
        db_index=True
    )
    price_id = models.CharField(
        max_length=200,
        db_index=True
    )

    contact_user_credits_per_day = models.IntegerField(
        db_index=True
    )
    alert_notification_credits_per_month = models.IntegerField(
        db_index=True
    )

class ContactUserCreditsBundle(Standard):
    """Contact user credits bundle.

    Updated: 12 September 2022, 10:27 PM
    """
    name = models.CharField(
        max_length=200,
        db_index=True
    )
    price_id = models.CharField(
        max_length=200,
        db_index=True
    )
    credits = models.IntegerField(
        db_index=True
    )
    expiry_days = models.IntegerField(
        db_index=True
    )
    plan_bonus_credits = models.IntegerField(
        db_index=True
    )

class AlertNotificationCreditsBundle(Standard):
    """Alert notification credits bundle.

    Updated: 12 September 2022, 10:27 PM
    """
    name = models.CharField(
        max_length=200,
        db_index=True
    )
    price_id = models.CharField(
        max_length=200,
        db_index=True
    )
    credits = models.IntegerField(
        db_index=True
    )
    expiry_days = models.IntegerField(
        db_index=True
    )
    plan_bonus_credits = models.IntegerField(
        db_index=True
    )

class UserSubscriptionPlan(Standard):
    """User subscription plan.

    Updated: 12 September 2022, 10:27 PM
    """
    user = models.ForeignKey(
        'relationships.User',
        related_name='user_subscription_plans',
        related_query_name='user_subscription_plans',
        on_delete=models.PROTECT,
        db_index=True
    )

    started = models.DateTimeField(
        db_index=True
    )
    renewed = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    expire = models.DateTimeField(
        db_index=True
    )
    plan = models.ForeignKey(
        'SubscriptionPlan',
        related_name='subscription_plans',
        related_query_name='subscription_plans',
        on_delete=models.PROTECT,
        db_index=True
    )
    last_plan = models.ForeignKey(
        'SubscriptionPlan',
        related_name='subscription_plans_as_last_plan',
        related_query_name='subscription_plans_as_last_plan',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )

    contact_user_credits_refreshed = models.DateTimeField(
        db_index=True
    )
    contact_user_credits = models.IntegerField(
        db_index=True
    )

    alert_notification_credits_refreshed = models.DateTimeField(
        db_index=True
    )
    alert_notification_credits = models.IntegerField(
        db_index=True
    )

class UserContactUserCreditsBundle(Standard):
    """User contact user credits bundle.

    Updated: 12 September 2022, 10:27 PM
    """
    user = models.ForeignKey(
        'relationships.User',
        related_name='user_contact_user_credits_bundles',
        related_query_name='user_contact_user_credits_bundles',
        on_delete=models.PROTECT,
        db_index=True
    )
    bundle = models.ForeignKey(
        'ContactUserCreditsBundle',
        related_name='user_contact_user_credits_bundles',
        related_query_name='user_contact_user_credits_bundles',
        on_delete=models.PROTECT,
        db_index=True
    )
    started = models.DateTimeField(
        db_index=True
    )
    expire = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    credits_added = models.IntegerField(
        db_index=True
    )
    credits_left = models.IntegerField(
        db_index=True
    )

class UserAlertNotificationCreditsBundle(Standard):
    """Alert notification credits bundle.

    Updated: 12 September 2022, 10:27 PM
    """
    user = models.ForeignKey(
        'relationships.User',
        related_name='alert_notification_credits_bundles',
        related_query_name='alert_notification_credits_bundles',
        on_delete=models.PROTECT,
        db_index=True
    )
    bundle = models.ForeignKey(
        'AlertNotificationCreditsBundle',
        related_name='alert_notification_credits_bundles',
        related_query_name='alert_notification_credits_bundles',
        on_delete=models.PROTECT,
        db_index=True
    )
    started = models.DateTimeField(
        db_index=True
    )
    expire = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    credits_added = models.IntegerField(
        db_index=True
    )
    credits_left = models.IntegerField(
        db_index=True
    )