import random, uuid

from relationships.constants.email_purposes import EMAIL_PURPOSE_CHOICES
from relationships.constants.whatsapp_purposes import WHATSAPP_PURPOSE_CHOICES

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User as django_user

from common import models as commods

from common.utilities.diff_now_desc import diff_now_desc

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

_TOKEN_LENGTH = 24
def get_token(length=_TOKEN_LENGTH):
    """Generates and returns a URL friendly token.

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
    for _ in range(0, length):
        p = random.randint(0, len(chars)-1)
        key += chars[p]
    return key

class PhoneNumberType(commods.Choice):
    """Phone number type.

    Last updated: 21 April 2021, 11:23 PM
    """
    pass

class PhoneNumber(commods.Standard):
    """Phone numbers.
    
    Last updated: 2 November 2021, 12:53 PM
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
        return f'+{self.country_code} {self.national_number}'

    def value(self):
        return f'{self.country_code}{self.national_number}'

    class Meta:
        unique_together = ['country_code', 'national_number']

class Email(commods.Standard):
    """Email.

    Last updated: 17 May 2022, 8:57 PM
    """

    do_not_email = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    email = commods.LowerCaseEmailField(
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

    # Not in use
    verified = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )

    def __str__(self):
        return f'{self.email}'

class InvalidEmail(commods.Standard):
    """Invalid email.

    Last updated: 21 April 2021, 11:13 PM
    """

    email = commods.LowerCaseCharField(
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
        return f'{self.email} [{self.id}]'

class User(commods.Standard):
    """User details.

    Last updated: 29 September 2022, 1:58 PM
    """
    registered = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    django_user = models.OneToOneField(
        django_user,
        related_name='user',
        related_query_name='user',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )

    walked_through_status = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )

    email = models.ForeignKey(
        'Email',
        related_name='user',
        related_query_name='user',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )
    first_name = models.CharField(
        max_length=20,
        db_index=True,
        null=True,
        blank=True
    )
    last_name = models.CharField(
        max_length=20,
        db_index=True,
        null=True,
        blank=True
    )
    phone_number = models.ForeignKey(
        'PhoneNumber',
        related_name='user',
        related_query_name='user',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )
    country = models.ForeignKey(
        'common.Country',
        related_name='users_as_country',
        related_query_name='users_as_country',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )
    business_name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        db_index=True
    )
    business_address = models.TextField(
        null=True,
        blank=True
    )
    business_description = models.TextField(
        null=True,
        blank=True
    )
    status_updated = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    status = models.TextField(
        null=True,
        blank=True
    )

    whatsapp_code_used = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    whatsapp_code = models.CharField(
        max_length=20,
        db_index=True,
        null=True,
        blank=True
    )
    whatsapp_code_generated = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    whatsapp_code_purpose = models.CharField(
        max_length=20,
        choices=WHATSAPP_PURPOSE_CHOICES,
        null=True,
        blank=True,
        db_index=True
    )

    pending_email = models.ForeignKey(
        'Email',
        related_name='user_as_pending_email',
        related_query_name='user_as_pending_email',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )
    email_code_used = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    email_code = models.CharField(
        max_length=20,
        db_index=True,
        null=True,
        blank=True
    )
    email_code_generated = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    email_code_purpose = models.CharField(
        max_length=20,
        choices=EMAIL_PURPOSE_CHOICES,
        null=True,
        blank=True,
        db_index=True
    )

    has_insights = models.BooleanField(
        null=True,
        blank=True
    )
    internal_notes = models.TextField(
        null=True,
        blank=True
    )

    def status_files(self):
        """Returns status files."""
        return StatusFile.objects\
            .filter(user=self, deleted__isnull=True, activated__isnull=False)\
            .order_by('-created')

    def status_updated_age_desc(self):
        return diff_now_desc(self.status_updated)

    def is_country_match_country_code(self):
        if self.phone_number is not None and self.country is not None:
            return self.country.country_code == self.phone_number.country_code

        return False

    def __str__(self):
        return f'{self.first_name} {self.last_name} [{self.id}]'

class UserAgent(commods.Standard):
    """User agent log.

    Last updated: 30 January 2022, 11:14 PM
    """
    user = models.ForeignKey(
        'User',
        related_name='user_agents',
        related_query_name='user_agents',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        db_index=True
    )
    is_routable = models.BooleanField(
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

    class Meta:
        unique_together = ['user', 'ip_address', 'is_routable', 'is_mobile',
            'is_tablet', 'is_touch_capable', 'is_pc', 'is_bot', 'browser',
            'browser_family', 'browser_version', 'browser_version_string', 'os',
            'os_family', 'os_version', 'os_version_string', 'device',
            'device_family']

class LoginAction(commods.Standard):
    """Login action.

    Last updated: 29 September 2022, 7:09 PM
    """
    user = models.ForeignKey(
        'User',
        related_name='login_actions',
        related_query_name='login_actions',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )
    type = models.CharField(
        max_length=40,
        choices=[
            ('magic', 'Magic Login'),
            ('whatsapp', 'WhatsApp Login')
        ],
        db_index=True
    )

class ContactAction(commods.Standard):
    """User contact action.
    
    Last updated: 29 September 2022, 7:07 PM
    """
    contactor = models.ForeignKey(
        'User',
        related_name='contact_actions',
        related_query_name='contact_actions',
        on_delete=models.PROTECT,
        db_index=True
    )
    phone_number = models.ForeignKey(
        'PhoneNumber',
        related_name='contact_actions',
        related_query_name='contact_actions',
        on_delete=models.PROTECT,
        db_index=True
    )
    action_count = models.IntegerField(
        default=0,
        db_index=True    
    )

    class Meta:
        unique_together = ('contactor', 'phone_number')

class DetailView(commods.Standard):
    """User detail view
    
    Last updated: 13 September 2022, 7:59 PM
    """
    viewee = models.ForeignKey(
        'User',
        related_name='user_detail_views',
        related_query_name='user_detail_views',
        on_delete=models.PROTECT,
        db_index=True
    )
    viewer = models.ForeignKey(
        'User',
        related_name='detail_views_as_viewer',
        related_query_name='detail_views_as_viewer',
        on_delete=models.PROTECT,
        db_index=True
    )
    count = models.IntegerField(
        default=0,
        db_index=True    
    )

class Review(commods.Standard):
    """Review

    Last updated: 29 September 2022, 7:01 PM
    """
    reviewer = models.ForeignKey(
        'User',
        related_name='reviews_as_reviewer',
        related_query_name='reviews_as_reviewer',
        on_delete=models.PROTECT,
        db_index=True
    )
    phone_number = models.ForeignKey(
        'PhoneNumber',
        related_name='reviews',
        related_query_name='reviews',
        on_delete=models.PROTECT,
        db_index=True
    )
    rating = models.CharField(
        max_length=40,
        choices=[
            ('good', 'Good Review'),
            ('bad', 'Bad Review')
        ],
        db_index=True
    )
    body = models.TextField()

    def response_count(self):
        return ReviewComment.objects.filter(review=self).count()

    def review_files(self):
        """Returns review files."""
        return ReviewFile.objects\
            .filter(reviewer=self.reviewer, phone_number=self.phone_number,
                deleted__isnull=True, activated__isnull=False)\
            .order_by('-created')

class ReviewFile(commods.Standard):
    """Review file

    Last updated: 17 October 2022, 7:22 PM
    """
    form_uuid = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    activated = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    file_uuid = models.UUIDField(
        null=True,
        blank=True,
        db_index=True
    )
    file = models.ForeignKey(
        'files.File',
        related_name='review_file_as_file',
        related_query_name='review_file_as_file',
        on_delete=models.PROTECT,
        db_index=True
    )
    phone_number = models.ForeignKey(
        'PhoneNumber',
        related_name='review_file_as_phone_number',
        related_query_name='review_file_as_phone_number',
        on_delete=models.PROTECT,
        db_index=True
    )
    reviewer = models.ForeignKey(
        'User',
        related_name='review_file_as_reviewer',
        related_query_name='review_file_as_reviewer',
        on_delete=models.PROTECT,
        db_index=True
    )

class ReviewComment(commods.Standard):
    """Review comment

    Last updated: 29 September 2022, 7:01 PM
    """
    review = models.ForeignKey(
        'Review',
        related_name='responses_as_review',
        related_query_name='responses_as_review',
        on_delete=models.PROTECT,
        db_index=True
    )
    author = models.ForeignKey(
        'User',
        related_name='review_responses_as_author',
        related_query_name='review_responses_as_author',
        on_delete=models.PROTECT,
        db_index=True
    )
    body = models.TextField()

class StatusFile(commods.Standard):
    """Status file

    Last updated: 29 September 2022, 7:01 PM
    """
    form_uuid = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    activated = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    user = models.ForeignKey(
        'User',
        related_name='status_files_as_user',
        related_query_name='status_files_as_user',
        on_delete=models.PROTECT,
        db_index=True
    )
    file_uuid = models.UUIDField(
        null=True,
        blank=True,
        db_index=True
    )
    file = models.ForeignKey(
        'files.File',
        related_name='status_files_as_file',
        related_query_name='status_files_as_file',
        on_delete=models.PROTECT,
        db_index=True
    )