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
    key = models.CharField(
        max_length=_USER_KEY_LENGTH,
        unique=True,
        default=get_user_key,
        db_index=True
    )
    phone_number = models.OneToOneField(
        'relationships.PhoneNumber',
        related_name='users',
        related_query_name='users',
        on_delete=models.PROTECT,
        db_index=True
    )

    name = models.CharField(
        max_length=100,
        db_index=True
    )

    email = models.ForeignKey(
        'relationships.Email',
        related_name='users',
        related_query_name='users',
        on_delete=models.PROTECT,
        db_index=True
    )

    def __str__(self):
        return f'({self.name} [{self.id}])'