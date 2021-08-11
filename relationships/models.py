import random
from django import db

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from common.models import (Standard, Choice, LowerCaseCharField,
    LowerCaseEmailField)
from chat.libraries.constants import methods

from hashid_field import HashidAutoField

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
    email = models.ForeignKey(
        'Email',
        related_name='phone_numbers',
        related_query_name='phone_numbers',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )

    def __str__(self):
        return f'(+{self.country_code} {self.national_number}, {self.user} \
[{self.id}])'

    class Meta:
        unique_together = ['country_code', 'national_number']

class Email(Standard):
    """Email.

    Last updated: 11 August 2021, 1:40 PM
    """

    email = LowerCaseEmailField(
        unique=True,
        db_index=True
    )

    name = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )

    notes = models.TextField(
        null=True,
        blank=True
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

    tags = models.ManyToManyField(
        'EmailTag',
        related_name='emails',
        related_query_name='emails',
        blank=True,
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

    Last updated: 1 July 2021, 5:57 PM
    """

    key = models.CharField(
        max_length=_USER_KEY_LENGTH,
        unique=True,
        default=get_user_key,
        db_index=True
    )
    phone_number = models.OneToOneField(
        'PhoneNumber',
        related_name='user',
        related_query_name='user',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
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
        null=True,
        blank=True,
        db_index=True
    )

    country = models.ForeignKey(
        'common.Country',
        related_name='users_w_this_country',
        related_query_name='users_w_this_country',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )
    state = models.ForeignKey(
        'common.State',
        related_name='users_w_this_state',
        related_query_name='users_w_this_state',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )

    current_match = models.ForeignKey(
        'Match',
        related_name='users_w_this_as_current_match',
        related_query_name='users_w_this_as_current_match',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )
    current_qna = models.ForeignKey(
        'QuestionAnswerPair',
        related_name='users_w_this_as_current_qna',
        related_query_name='users_w_this_as_current_qna',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )

    def __str__(self):
        return f'({self.name} [{self.id}])'

class PhoneNumberHash(Standard):
    """A URL sent to a user of a phone number. A URL has a standard base, and a
    unique hash, and each URL is unique to auser-phone-number, so we may track
    access of the URL. We use a hash and not the ID straight to prevent users
    from iterating the IDs in the URL.

    Last updated: 18 June 2021, 3:53 PM
    """

    id = HashidAutoField(primary_key=True)
    expired = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )

    user = models.ForeignKey(
        'User',
        related_name='phone_number_hashes',
        related_query_name='phone_number_hashes',
        on_delete=models.PROTECT,
        db_index=True
    )
    phone_number_type = models.ForeignKey(
        'PhoneNumberType',
        related_name='phone_number_hashes',
        related_query_name='phone_number_hashes',
        on_delete=models.PROTECT,
        db_index=True
    )
    phone_number = models.ForeignKey(
        'PhoneNumber',
        related_name='phone_number_hashes',
        related_query_name='phone_number_hashes',
        on_delete=models.PROTECT,
        db_index=True
    )

    class Meta:
        verbose_name = 'Phone number hash'
        verbose_name_plural = 'Phone number hashes'
        unique_together = ['user', 'phone_number_type', 'phone_number']
        index_together = ['user', 'phone_number_type', 'phone_number']
    
    def __str__(self):
        return f'({self.user}, {self.phone_number_type}, {self.phone_number} [{self.id}])'

PHONE_NUMBER_ACCESS_SUCCESSFUL = 'PHONE_NUMBER_ACCESS_SUCCESSFUL'
PHONE_NUMBER_ACCESS_FAILED = 'PHONE_NUMBER_ACCESS'
class PhoneNumberLinkAccess(Standard):
    """A single access of a phone number hash/URL.

    Last updated: 17 July 2021, 10:12 PM
    """
    accessed = models.DateTimeField(
        db_index=True,
        auto_now=True
    )
    outcome = models.CharField(
        max_length=200,
        choices=[
            (PHONE_NUMBER_ACCESS_SUCCESSFUL, PHONE_NUMBER_ACCESS_SUCCESSFUL),
            (PHONE_NUMBER_ACCESS_FAILED, PHONE_NUMBER_ACCESS_FAILED),
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
        'PhoneNumberHash',
        related_name='accesses',
        related_query_name='accesses',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Phone Number URL access'
        verbose_name_plural = 'Phone Number URL accesses'

class UnitOfMeasure(Standard, Choice):
    """Unit of measure. Description is displayed to user.

    Last updated: 27 May 2021, 10:14 PM
    """
    priority = models.IntegerField(
        default=0,
        db_index=True
    )
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

class Availability(Choice):
    """Availability. E.g., ready stock, OTG.

    Last updated: 12 May 2021, 1:27 PM
    """
    
    class Meta:
        verbose_name_plural = 'availabilities'

class ProductType(Choice):
    """Product type.

    Last updated: 12 May 2021, 1:39 PM
    """
    pass

class Connection(Choice):
    """Connection.

    Last updated: 7 June 2021, 9:36 PM
    """
    user_1 = models.ForeignKey(
        'User',
        related_name='connection_user_1s',
        related_query_name='connection_user_1s',
        on_delete=models.PROTECT,
        db_index=True
    )
    user_2 = models.ForeignKey(
        'User',
        related_name='connection_user_2s',
        related_query_name='connection_user_2s',
        on_delete=models.PROTECT,
        db_index=True
    )

    def clean(self):
        super(Connection, self).clean()

        # user_1's ID must be smaller than user_2's
        if self.user_1.id > self.user_2.id:
            raise ValidationError('user_1.id must be smaller than user_2.id')

TIMEFRAME_DURATION_UOM = [
    ('d', 'Day'),
    ('w', 'Week'),
    ('m', 'Month')
]
class TimeFrame(Standard):
    """Time frame.

    Last updated: 12 May 2021, 4:03 PM
    """
    duration_uom = models.CharField(
        max_length=2,
        choices=TIMEFRAME_DURATION_UOM,
        db_index=True
    )
    duration = models.FloatField(
        null=True,
        blank=True,
        db_index=True
    )
    deadline = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )

    def clean(self):
        super(TimeFrame, self).clean()

        # Either supply_quote or demand_quote must be set.
        if (self.duration_uom is None and self.duration is None) and \
            self.deadline:
            raise ValidationError('Either duration/uom or deadline must be \
                set.')

class Match(Standard):
    """Match between supply and demand.

    Last updated: 24 June 2021, 10:05 PM
    """
    closed = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    ready = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )

    sent_buyer_confirm_interest = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    sent_buyer_confirm_interest_message = models.ForeignKey(
        'chat.TwilioOutboundMessage',
        related_name='matches_w_this_buyer_confirm_interest_value',
        related_query_name='matches_w_this_buyer_confirm_interest_value',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )

    sent_seller_confirm_interest = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    sent_seller_confirm_interest_message = models.ForeignKey(
        'chat.TwilioOutboundMessage',
        related_name='matches_w_this_seller_confirm_interest_message',
        related_query_name='matches_w_this_seller_confirm_interest_message',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )

    buyer_confirmed_interest = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    buyer_interested = models.BooleanField(
        null=True,
        blank=True,
        db_index=True
    )
    buyer_confirmed_interest_value = models.ForeignKey(
        'chat.MessageDataValue',
        related_name='matches_w_this_buyer_confirmed_interest_value',
        related_query_name='matches_w_this_buyer_confirmed_interest_value',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )

    seller_confirmed_interest = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    seller_interested = models.BooleanField(
        null=True,
        blank=True,
        db_index=True
    )
    seller_confirmed_interest_value = models.ForeignKey(
        'chat.MessageDataValue',
        related_name='matches_w_this_seller_confirmed_value',
        related_query_name='matches_w_this_seller_confirmed_value',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )

    buyer_confirmed_details = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    buyer_confirmed_details_correct = models.BooleanField(
        null=True,
        blank=True,
        db_index=True
    )
    buyer_confirmed_details_correct_value = models.ForeignKey(
        'chat.MessageDataValue',
        related_name='matches_w_this_buyer_confirmed_details_correct_value',
        related_query_name=\
            'matches_w_this_buyer_confirmed_details_correct_value',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )

    seller_confirmed_details = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    seller_confirmed_details_correct = models.BooleanField(
        null=True,
        blank=True,
        db_index=True
    )
    seller_confirmed_details_correct_value = models.ForeignKey(
        'chat.MessageDataValue',
        related_name='matches_w_this_seller_confirmed_details_correct_value',
        related_query_name=\
            'matches_w_this_seller_confirmed_details_correct_value',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )

    buyer_confirmed_still_interested = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    buyer_still_interested = models.BooleanField(
        null=True,
        blank=True,
        db_index=True
    )
    buyer_still_interested_value = models.ForeignKey(
        'chat.MessageDataValue',
        related_name='matches_w_this_buyer_still_interested_value',
        related_query_name='matches_w_this_buyer_still_interested_value',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )

    seller_confirmed_still_interested = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    seller_still_interested = models.BooleanField(
        null=True,
        blank=True,
        db_index=True
    )
    seller_still_interested_value = models.ForeignKey(
        'chat.MessageDataValue',
        related_name='matches_w_this_seller_still_interested_value',
        related_query_name='matches_w_this_seller_still_interested_value',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )

    buyer_stopped_discussion = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    buyer_stopped_discussion_value = models.ForeignKey(
        'chat.MessageDataValue',
        related_name='matches_w_this_buyer_stopped_discussion_value',
        related_query_name='matches_w_this_buyer_stopped_discussion_value',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )

    seller_stopped_discussion = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    seller_stopped_discussion_value = models.ForeignKey(
        'chat.MessageDataValue',
        related_name='matches_w_this_seller_stopped_discussion_value',
        related_query_name='matches_w_this_seller_stopped_discussion_value',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )

    buyer_bought_contact = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    buyer_payment_hash = models.ForeignKey(
        'payments.PaymentHash',
        related_name='matches_w_this_buyer_payment_hash',
        related_query_name='matches_w_this_buyer_payment_hash',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )

    seller_bought_contact = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    seller_payment_hash = models.ForeignKey(
        'payments.PaymentHash',
        related_name='matches_w_this_seller_payment_hash',
        related_query_name='matches_w_this_seller_payment_hash',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )

    sent_contact_to_buyer = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    sent_contact_to_seller = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )

    supply = models.ForeignKey(
        'Supply',
        related_name='matches',
        related_query_name='matches',
        on_delete=models.PROTECT,
        db_index=True
    )
    demand = models.ForeignKey(
        'Demand',
        related_name='matches',
        related_query_name='matches',
        on_delete=models.PROTECT,
        db_index=True
    )

    def __str__(self):
        return f'({self.supply}, {self.demand}, [{self.id}])'

    class Meta:
        verbose_name_plural = 'matches'

class Supply(Standard):
    """Supply.

    Last updated: 20 June 2021, 4:28 PM
    """
    user = models.ForeignKey(
        'User',
        related_name='supplies',
        related_query_name='supplies',
        on_delete=models.PROTECT,
        db_index=True
    )

    product_type_data_value = models.ForeignKey(
        'chat.MessageDataValue',
        related_name='supply_product_type_values',
        related_query_name='supply_product_type_values',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )
    product_type_method = models.CharField(
        max_length=200,
        choices=methods.choices,
        null=True,
        blank=True,
        db_index=True
    )
    product_type = models.ForeignKey(
        'ProductType',
        related_name='supplies',
        related_query_name='supplies',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )

    country_data_value = models.ForeignKey(
        'chat.MessageDataValue',
        related_name='supply_country_values',
        related_query_name='supply_country_values',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )
    country_method = models.CharField(
        max_length=200,
        choices=methods.choices,
        null=True,
        blank=True,
        db_index=True
    )
    country = models.ForeignKey(
        'common.Country',
        related_name='supplies',
        related_query_name='supplies',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )
    state_data_value = models.ForeignKey(
        'chat.MessageDataValue',
        related_name='supply_state_values',
        related_query_name='supply_state_values',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )
    state_method = models.CharField(
        max_length=200,
        choices=methods.choices,
        null=True,
        blank=True,
        db_index=True
    )
    state = models.ForeignKey(
        'common.State',
        related_name='supplies',
        related_query_name='supplies',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )

    availability_data_value = models.ForeignKey(
        'chat.MessageDataValue',
        related_name='supply_availability_values',
        related_query_name='supply_availability_values',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )
    availability_method = models.CharField(
        max_length=200,
        choices=methods.choices,
        null=True,
        blank=True,
        db_index=True
    )
    availability = models.ForeignKey(
        'Availability',
        related_name='supplies',
        related_query_name='supplies',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )

    packing_data_value = models.ForeignKey(
        'chat.MessageDataValue',
        related_name='supply_packing_values',
        related_query_name='supply_packing_values',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )
    packing_method = models.CharField(
        max_length=200,
        choices=methods.choices,
        null=True,
        blank=True,
        db_index=True
    )
    packing = models.ForeignKey(
        'UnitOfMeasure',
        related_name='supplies',
        related_query_name='supplies',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )

    quantity_data_value = models.ForeignKey(
        'chat.MessageDataValue',
        related_name='supply_quantity_values',
        related_query_name='supply_quantity_values',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )
    quantity_method = models.CharField(
        max_length=200,
        choices=methods.choices,
        null=True,
        blank=True,
        db_index=True
    )
    quantity = models.FloatField(
        null=True,
        blank=True,
        db_index=True
    )

    pre_order_timeframe_data_value = models.ForeignKey(
        'chat.MessageDataValue',
        related_name='supply_pre_order_timeframe_values',
        related_query_name='supply_pre_order_timeframe_values',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )
    pre_order_timeframe_method = models.CharField(
        max_length=200,
        choices=methods.choices,
        null=True,
        blank=True,
        db_index=True
    )
    pre_order_timeframe = models.ForeignKey(
        'TimeFrame',
        related_name='supplies',
        related_query_name='supplies',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )

    price_data_value = models.ForeignKey(
        'chat.MessageDataValue',
        related_name='supply_price_values',
        related_query_name='supply_price_values',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )
    price_method = models.CharField(
        max_length=200,
        choices=methods.choices,
        null=True,
        blank=True,
        db_index=True
    )    
    price = models.FloatField(
        null=True,
        blank=True
    )
    currency_data_value = models.ForeignKey(
        'chat.MessageDataValue',
        related_name='supply_currency_values',
        related_query_name='supply_currency_values',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )
    currency_method = models.CharField(
        max_length=200,
        choices=methods.choices,
        null=True,
        blank=True,
        db_index=True
    )  
    currency = models.ForeignKey(
        'payments.Currency',
        related_name='supplies',
        related_query_name='supplies',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )

    deposit_percentage_data_value = models.ForeignKey(
        'chat.MessageDataValue',
        related_name='supply_deposit_percentage_values',
        related_query_name='supply_deposit_percentage_values',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )
    deposit_percentage_method = models.CharField(
        max_length=200,
        choices=methods.choices,
        null=True,
        blank=True,
        db_index=True
    )  
    deposit_percentage = models.FloatField(
        null=True,
        blank=True
    )

    accept_lc_data_value = models.ForeignKey(
        'chat.MessageDataValue',
        related_name='supply_accept_lc_values',
        related_query_name='supply_accept_lc_values',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )
    accept_lc_method = models.CharField(
        max_length=200,
        choices=methods.choices,
        null=True,
        blank=True,
        db_index=True
    )  
    accept_lc = models.BooleanField(
        null=True,
        blank=True
    )

    previous_version = models.ForeignKey(
        'Supply',
        related_name='next_versions_of_this_supply',
        related_query_name='next_versions_of_this_supply',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )
    next_version = models.ForeignKey(
        'Supply',
        related_name='previous_versions_of_this_supply',
        related_query_name='previous_versions_of_this_supply',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )

    def __str__(self):
        return f'({self.product_type_data_value}, {self.quantity_data_value}, \
            {self.price_data_value}, [{self.id}])'

    class Meta:
        verbose_name_plural = 'supplies'

class Demand(Standard):
    """Demand.

    Last updated: 20 June 2021, 5:49 PM
    """
    user = models.ForeignKey(
        'User',
        related_name='demands',
        related_query_name='demands',
        on_delete=models.PROTECT,
        db_index=True
    )

    product_type_data_value = models.ForeignKey(
        'chat.MessageDataValue',
        related_name='demand_product_type_values',
        related_query_name='demand_product_type_values',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )
    product_type_method = models.CharField(
        max_length=200,
        choices=methods.choices,
        null=True,
        blank=True,
        db_index=True
    )
    product_type = models.ForeignKey(
        'ProductType',
        related_name='demands',
        related_query_name='demands',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )

    country_data_value = models.ForeignKey(
        'chat.MessageDataValue',
        related_name='demand_country_values',
        related_query_name='demand_country_values',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )
    country_method = models.CharField(
        max_length=200,
        choices=methods.choices,
        null=True,
        blank=True,
        db_index=True
    )
    country = models.ForeignKey(
        'common.Country',
        related_name='demands',
        related_query_name='demands',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )
    state_data_value = models.ForeignKey(
        'chat.MessageDataValue',
        related_name='demand_state_values',
        related_query_name='demand_state_values',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )
    state_method = models.CharField(
        max_length=200,
        choices=methods.choices,
        null=True,
        blank=True,
        db_index=True
    )
    state = models.ForeignKey(
        'common.State',
        related_name='demands',
        related_query_name='demands',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )

    packing_data_value = models.ForeignKey(
        'chat.MessageDataValue',
        related_name='demand_packing_values',
        related_query_name='demand_packing_values',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )
    packing_method = models.CharField(
        max_length=200,
        choices=methods.choices,
        null=True,
        blank=True,
        db_index=True
    )
    packing = models.ForeignKey(
        'UnitOfMeasure',
        related_name='demands',
        related_query_name='demands',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )

    quantity_data_value = models.ForeignKey(
        'chat.MessageDataValue',
        related_name='demand_quantity_values',
        related_query_name='demand_quantity_values',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )
    quantity_method = models.CharField(
        max_length=200,
        choices=methods.choices,
        null=True,
        blank=True,
        db_index=True
    )
    quantity = models.FloatField(
        null=True,
        blank=True,
        db_index=True
    )

    price_data_value = models.ForeignKey(
        'chat.MessageDataValue',
        related_name='demand_price_values',
        related_query_name='demand_price_values',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )
    price_method = models.CharField(
        max_length=200,
        choices=methods.choices,
        null=True,
        blank=True,
        db_index=True
    )
    price = models.FloatField(
        null=True,
        blank=True
    )
    currency_data_value = models.ForeignKey(
        'chat.MessageDataValue',
        related_name='demand_currency_values',
        related_query_name='demand_currency_values',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )
    currency_method = models.CharField(
        max_length=200,
        choices=methods.choices,
        null=True,
        blank=True,
        db_index=True
    )
    currency = models.ForeignKey(
        'payments.Currency',
        related_name='demands',
        related_query_name='demands',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )

    previous_version = models.ForeignKey(
        'Demand',
        related_name='next_versions_of_this_demand',
        related_query_name='next_versions_of_this_demand',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )
    next_version = models.ForeignKey(
        'Demand',
        related_name='previous_versions_of_this_demand',
        related_query_name='previous_versions_of_this_demand',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )

    def __str__(self):
        return f'({self.product_type_data_value}, {self.quantity_data_value}, \
            {self.price_data_value}, [{self.id}])'

class QuestionAnswerPair(Standard):
    """Question-answer pair.

    Last updated: 24 June 2021, 11:28 PM
    """
    questioner = models.ForeignKey(
        'User',
        related_name='qnas_w_this_questioner',
        related_query_name='qnas_w_this_questioner',
        on_delete=models.PROTECT,
        db_index=True
    )
    answerer = models.ForeignKey(
        'User',
        related_name='qnas_w_this_answerer',
        related_query_name='qnas_w_this_answerer',
        on_delete=models.PROTECT,
        db_index=True
    )

    asked = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    question_auto_cleaned = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    question_ready = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    question_forwarded = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    answered = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    answer_auto_cleaned = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    answer_ready = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    answer_forwarded = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )

    question_captured_value = models.ForeignKey(
        'chat.MessageDataValue',
        related_name='qnas_w_this_question_captured_value',
        related_query_name='qnas_w_this_question_captured_value',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    question_forwarded_message = models.ForeignKey(
        'chat.TwilioOutboundMessage',
        related_name='qnas_w_this_question_forwarded_message',
        related_query_name='qnas_w_this_question_forwarded_message',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    auto_cleaned_question_w_mark_up = models.TextField(
        null=True,
        blank=True
    )
    auto_cleaned_question = models.TextField(
        null=True,
        blank=True
    )
    manual_cleaned_question = models.TextField(
        null=True,
        blank=True
    )
    use_auto_cleaned_question = models.BooleanField(
        null=True,
        blank=True
    )

    answer_captured_value = models.ForeignKey(
        'chat.MessageDataValue',
        related_name='qnas_w_this_answer_captured_value',
        related_query_name='qnas_w_this_answer_captured_value',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    answer_forwarded_message = models.ForeignKey(
        'chat.TwilioOutboundMessage',
        related_name='qnas_w_this_answer_forwarded_message',
        related_query_name='qnas_w_this_answer_forwarded_message',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    auto_cleaned_answer_w_mark_up = models.TextField(
        null=True,
        blank=True
    )
    auto_cleaned_answer = models.TextField(
        null=True,
        blank=True
    )
    manual_cleaned_answer = models.TextField(
        null=True,
        blank=True
    )
    use_auto_cleaned_answer = models.BooleanField(
        null=True,
        blank=True
    )

    match = models.ForeignKey(
        'Match',
        related_name='question_answer_pairs',
        related_query_name='question_answer_pairs',
        on_delete=models.PROTECT,
        db_index=True
    )

class EmailTag(Choice):
    """Email tag

    Last updated: 11 August 2021, 1:30 PM
    """
    pass