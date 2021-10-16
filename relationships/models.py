import random

from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.deletion import PROTECT
from django.utils.translation import gettext_lazy as _

from common.models import (Standard, Choice, LowerCaseCharField,
    LowerCaseEmailField)
from chat.libraries.constants import datas, methods

import django.contrib.auth.models as authmods

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

    def __str__(self):
        return f'(+{self.country_code} {self.national_number}, [{self.id}])'

    class Meta:
        unique_together = ['country_code', 'national_number']

class PhoneNumberVerification(Standard):
    """Verification record for a phone number..

    Last updated: 15 October 2021, 11:05 PM
    """
    verified = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    phone_number = models.ForeignKey(
        'PhoneNumber',
        related_name='verifications',
        related_query_name='verifications',
        on_delete=models.PROTECT,
        db_index=True
    )
    phone_number_type = models.ForeignKey(
        'PhoneNumberType',
        related_name='verifications',
        related_query_name='verifications',
        on_delete=models.PROTECT,
        db_index=True
    )

    def __str__(self):
        return f'({self.phone_number} [{self.id}])'

class Email(Standard):
    """Email.

    Last updated: 15 October 2021, 11:05 PM
    """

    verified = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    email = LowerCaseEmailField(
        unique=True,
        db_index=True
    )
    notes = models.TextField(
        null=True,
        blank=True
    )
    invalid_email = models.ForeignKey(
        'relationships.InvalidEmail',
        related_name='clean_email',
        related_query_name='clean_email',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
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

    Last updated: 15 October 2021, 11:08 PM
    """
    profile_picture = models.ForeignKey(
        'files.File',
        related_name='users_w_this_profile_picture',
        related_query_name='users_w_this_profile_picture',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )
    key = models.CharField(
        max_length=_USER_KEY_LENGTH,
        unique=True,
        default=get_user_key,
        db_index=True
    )
    first_given_name = models.CharField(
        max_length=20,
        db_index=True
    )
    last_family_name = models.CharField(
        max_length=20,
        db_index=True
    )
    display_family_name_first = models.BooleanField(
        db_index=True,
        blank=True,
        null=True
    )
    description = models.TextField(blank=True, null=True)

    languages = models.ManyToManyField(
        'common.Language',
        related_name='users_w_this_language',
        related_query_name='users_w_this_language',
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
    state_string = models.CharField(
        max_length=50,
        null=True,
        blank=True,
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
        return f'({self.name}, {self.email}, {self.phone_number} [{self.id}])'

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

class Connection(Standard):
    """Connection between two user.

    Last updated: 15 October 2021, 11:56 PM
    """
    created = models.DateTimeField(
        db_index=True,
        auto_now=True
    )
    user_one = models.ForeignKey(
        'User',
        related_name='users_with_this_connection_as_one',
        related_query_name='users_with_this_connection_as_one',
        on_delete=models.PROTECT,
        db_index=True
    )
    user_two = models.ForeignKey(
        'User',
        related_name='users_with_this_connection_as_two',
        related_query_name='users_with_this_connection_as_two',
        on_delete=models.PROTECT,
        db_index=True
    )
    
    def clean(self):
        super(Connection, self).clean()

        # user_one's ID must be smaller than user_two's
        if self.user_one.id > self.user_two.id:
            raise ValidationError(
                'user_one.id must be smaller than user_two.id')

    class Meta:
        unique_together = ['user_one', 'user_two']

class FriendRequest(Standard):
    """Friend request.

    Last updated: 15 October 2021, 11:56 PM
    """
    requested = models.DateTimeField(db_index=True)
    requester = models.ForeignKey(
        'User',
        related_name='users_with_this_friend_requester_as_requester',
        related_query_name='users_with_this_friend_requester_as_requester',
        on_delete=models.PROTECT,
        db_index=True
    )
    requestee = models.ForeignKey(
        'User',
        related_name='users_with_this_friend_requester_as_requestee',
        related_query_name='users_with_this_friend_requester_as_requestee',
        on_delete=models.PROTECT,
        db_index=True
    )
    responded = models.DateTimeField(db_index=True)
    response = models.CharField(
        max_length=20,
        choices=[
            ('accept', 'Accept'),
            ('reject', 'Reject')
        ],
        null=True,
        blank=True
    )