from django.db import models
from django.db.models.fields import BLANK_CHOICE_DASH
from django.db.models.fields.related import ForeignKey
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

    Last updated: 15 May 2021, 4:34 PM
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

    Last updated: 12 May 2021, 2:35 PM
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

class TimeFrame(Standard):
    """Time frame.

    Last updated: 12 May 2021, 4:03 PM
    """
    duration_uom = models.CharField(
        max_length=2,
        choices=[
            ('d', 'Day'),
            ('w', 'Week'),
            ('m', 'Month')
        ],
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

class Match(Choice):
    """Match between supply and demand.

    Last updated: 12 May 2021, 2:40 PM
    """
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

    class Meta:
        verbose_name_plural = 'matches'

class Supply(Standard):
    """Supply.

    Last updated: 12 May 2021, 6:14 PM
    """
    user = models.ForeignKey(
        'User',
        related_name='supplies',
        related_query_name='supplies',
        on_delete=models.PROTECT,
        db_index=True
    )

    product_type_captured = models.TextField(
        null=True,
        blank=True
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

    country_state_captured = models.TextField(
        null=True,
        blank=True        
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
    state = models.ForeignKey(
        'common.State',
        related_name='supplies',
        related_query_name='supplies',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )

    availability_captured = models.TextField(
        null=True,
        blank=True        
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

    packing_captured = models.TextField(
        null=True,
        blank=True        
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

    quantity_captured = models.TextField(
        null=True,
        blank=True
    )
    quantity = models.FloatField(
        null=True,
        blank=True,
        db_index=True
    )

    preorder_timeframe_captured = models.TextField(
        null=True,
        blank=True
    )
    preorder_timeframe = models.ForeignKey(
        'TimeFrame',
        related_name='supplies',
        related_query_name='supplies',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )

    price_captured = models.TextField(
        null=True,
        blank=True
    )
    price = models.FloatField(
        null=True,
        blank=True
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

    deposit_percentage_captured = models.TextField(
        null=True,
        blank=True
    )
    deposit_percentage = models.FloatField(
        null=True,
        blank=True
    )

    accept_lc_captured = models.TextField(
        null=True,
        blank=True
    )
    accept_lc = models.BooleanField(
        null=True,
        blank=True
    )

    previous_version = models.ForeignKey(
        'Supply',
        related_name='supply_previous_versions',
        related_query_name='supply_previous_versions',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )
    next_version = models.ForeignKey(
        'Supply',
        related_name='supply_next_versions',
        related_query_name='supply_next_versions',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )

    class Meta:
        verbose_name_plural = 'supplies'

class Demand(Standard):
    """Demand.

    Last updated: 12 May 2021, 4:12 PM
    """
    user = models.ForeignKey(
        'User',
        related_name='demands',
        related_query_name='demands',
        on_delete=models.PROTECT,
        db_index=True
    )

    product_type_captured = models.TextField(
        null=True,
        blank=True
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

    country_state_captured = models.TextField(
        null=True,
        blank=True        
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
    state = models.ForeignKey(
        'common.State',
        related_name='demands',
        related_query_name='demands',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )

    packing_captured = models.TextField(
        null=True,
        blank=True        
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

    quantity_captured = models.TextField(
        null=True,
        blank=True
    )
    quantity = models.FloatField(
        null=True,
        blank=True,
        db_index=True
    )

    price_captured = models.TextField(
        null=True,
        blank=True
    )
    price = models.FloatField(
        null=True,
        blank=True
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
        related_name='demand_previous_versions',
        related_query_name='demand_previous_versions',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )
    next_version = models.ForeignKey(
        'Demand',
        related_name='demand_next_versions',
        related_query_name='demand_next_versions',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )

class QuestionAnswerPair(Standard):
    """Question-answer pair.

    Last updated: 12 May 2021, 5:27 PM
    """
    asker = models.ForeignKey(
        'User',
        related_name='question_answer_pair_askers',
        related_query_name='question_answer_pair_askers',
        on_delete=models.PROTECT,
        db_index=True
    )
    answerer = models.ForeignKey(
        'User',
        related_name='question_answer_pair_answerers',
        related_query_name='question_answer_pair_answerers',
        on_delete=models.PROTECT,
        db_index=True
    )

    asked = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    sent_answerer = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    answered = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )

    question_captured = models.TextField()
    question_rewrote = models.TextField(
        null=True,
        blank=True
    )

    answer_captured = models.TextField(
        null=True,
        blank=True,
        db_index=True
    )
    answer_rewrote = models.TextField(
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