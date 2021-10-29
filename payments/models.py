from django.db import models
from common.models import Standard, Choice
from hashid_field import HashidAutoField

# TODO: Dropped everything, we'll recreate them when we get back to payments.

# class PaymentHash(Standard):
#     """Hash of payment link sent to user.

#     Last updated: 15 July 2021, 4:04
#     """

#     id = HashidAutoField(primary_key=True)
#     expired = models.DateTimeField(
#         null=True,
#         blank=True,
#         db_index=True
#     )

#     user = models.ForeignKey(
#         'relationships.User',
#         related_name='payment_links',
#         related_query_name='payment_links',
#         on_delete=models.PROTECT,
#         db_index=True
#     )
#     # match = models.ForeignKey(
#     #     'relationships.Match',
#     #     related_name='payment_links',
#     #     related_query_name='payment_links',
#     #     on_delete=models.PROTECT,
#     #     db_index=True
#     # )
    
#     started = models.DateTimeField(
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     succeeded = models.DateTimeField(
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     failed = models.DateTimeField(
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     session_id = models.CharField(
#         max_length=200,
#         null=True,
#         blank=True,
#         db_index=True        
#     )

#     price = models.ForeignKey(
#         'Price',
#         null=True,
#         blank=True,
#         related_name='payment_hashes',
#         related_query_name='payment_hashes',
#         on_delete=models.PROTECT,
#         db_index=True
#     )
    
#     def __str__(self):
#         return f'({self.user}, {self.price} [{self.id}])'

#     class Meta:
#         # Match is deleted
#         # unique_together = ('user', 'match')
#         verbose_name = 'Payment hash'
#         verbose_name_plural = 'Payment hashes'

# class PaymentEvent(Standard):
#     """Payment event.

#     Last updated: 17 June 2021, 5:55 PM
#     """

#     event_type = models.ForeignKey(
#         'PaymentEventType',
#         related_name='payment_events',
#         related_query_name='payment_events',
#         on_delete=models.PROTECT,
#         db_index=True
#     )
#     currency = models.ForeignKey(
#         'Currency',
#         related_name='payment_events',
#         related_query_name='payment_events',
#         on_delete=models.PROTECT,
#         db_index=True
#     )	
#     amount = models.FloatField(db_index=True)
	
#     user = models.ForeignKey(
#         'relationships.User',
#         related_name='payment_events',
#         related_query_name='payment_events',
#         on_delete=models.PROTECT,
#         db_index=True
#     )
#     payment_hash = models.ForeignKey(
#         'PaymentHash',
#         related_name='payment_events',
#         related_query_name='payment_events',
#         on_delete=models.PROTECT,
#         db_index=True
#     )

#     def __str__(self):
#         return f'({self.user}, {self.amount}, {self.currency} \
#             [{self.id}])'

# class PaymentEventType(Choice):
#     """Payment event type.

#     Last updated: 25 April 2021, 4:11 PM
#     """
#     pass

# class Currency(Choice):
#     """Currency. E.g., USD.

#     Last updated: 23 April 2021, 6:52 PM
#     """

#     class Meta:
#         verbose_name = 'Currency'
#         verbose_name_plural = 'Currencies'

# PAYMENT_LINK_ACCESS_SUCCESSFUL = 'PAYMENT_LINK_ACCESS_SUCCESSFUL'
# PAYMENT_LINK_ACCESS_FAILED = 'PAYMENT_LINK_ACCESS_FAILED'
# class PaymentLinkAccess(Standard):
#     """A single access of a payment hash/URL.

#     Last updated: 18 June 2021, 2:35 PM
#     """
#     accessed = models.DateTimeField(
#         db_index=True,
#         auto_now=True
#     )
#     outcome = models.CharField(
#         max_length=200,
#         choices=[
#             (PAYMENT_LINK_ACCESS_SUCCESSFUL, PAYMENT_LINK_ACCESS_SUCCESSFUL),
#             (PAYMENT_LINK_ACCESS_FAILED, PAYMENT_LINK_ACCESS_FAILED),
#         ],
#         null=True,
#         blank=True,
#         db_index=True
#     )
        
#     ip_address = models.GenericIPAddressField(
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     is_mobile = models.BooleanField(
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     is_tablet = models.BooleanField(
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     is_touch_capable = models.BooleanField(
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     is_pc = models.BooleanField(
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     is_bot = models.BooleanField(
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     browser = models.CharField(
#         max_length=200,
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     browser_family = models.CharField(
#         max_length=200,
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     browser_version = models.CharField(
#         max_length=200,
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     browser_version_string = models.CharField(
#         max_length=200,
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     os = models.CharField(
#         max_length=200,
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     os_family = models.CharField(
#         max_length=200,
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     os_version = models.CharField(
#         max_length=200,
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     os_version_string = models.CharField(
#         max_length=200,
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     device = models.CharField(
#         max_length=200,
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     device_family = models.CharField(
#         max_length=200,
#         null=True,
#         blank=True,
#         db_index=True
#     )
        
#     hash = models.ForeignKey(
#         'PaymentHash',
#         related_name='accesses',
#         related_query_name='accesses',
#         on_delete=models.PROTECT,
#         db_index=True
#     )

#     class Meta:
#         verbose_name = 'Phone hash access'
#         verbose_name_plural = 'Phone hash accesses'

# class Price(Choice):
#     """Prices (of products) available for purchase - e.g., USD 1 referral fee.

#     Last updated: 30 July 2021, 11:52 PM
#     """

#     display_name = models.CharField(
#         max_length=200,
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     value = models.FloatField(
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     currency = models.ForeignKey(
#         'Currency',
#         related_name='prices',
#         related_query_name='prices',
#         null=True,
#         blank=True,
#         on_delete=models.PROTECT,
#         db_index=True
#     )

#     class Meta:
#         verbose_name = 'Price'
#         verbose_name_plural = 'Prices'

# StripeCallbackCheckoutSession_Paid = 'paid'
# StripeCallbackCheckoutSession_Unpaid = 'unpaid'
# StripeCallbackCheckoutSession_NoPaymentRequired = 'no_payment_required'
# class StripeCallbackCheckoutSession(Standard):
#     """Stripe callback checkout session details
    
#     Last updated: 15 July 2021, 4:38 PM
#     """
#     session_id = models.CharField(
#         max_length=200,
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     amount_total = models.IntegerField(
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     currency = models.CharField(
#         max_length=200,
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     customer = models.CharField(
#         max_length=200,
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     customer_details_email = models.CharField(
#         max_length=200,
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     mode = models.CharField(
#         max_length=200,
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     payment_intent = models.CharField(
#         max_length=200,
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     payment_status = models.CharField(
#         max_length=200,
#         null=True,
#         blank=True,
#         db_index=True,
#         choices=[
#             (StripeCallbackCheckoutSession_Paid, \
#                 StripeCallbackCheckoutSession_Paid),
#             (StripeCallbackCheckoutSession_Unpaid, \
#                 StripeCallbackCheckoutSession_Unpaid),
#             (StripeCallbackCheckoutSession_NoPaymentRequired, \
#                 StripeCallbackCheckoutSession_NoPaymentRequired)
#         ]
#     )
#     success_url = models.CharField(
#         max_length=200,
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     cancel_url = models.CharField(
#         max_length=200,
#         null=True,
#         blank=True,
#         db_index=True
#     )
