import random

from relationships.constants.email_purposes import EMAIL_PURPOSE_CHOICES
from relationships.constants.whatsapp_purposes import WHATSAPP_PURPOSE_CHOICES

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User as django_user

from common import models as commods

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
        return f'+{self.country_code} {self.national_number}'

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
    register_cookie_uuid = models.CharField(
        max_length=50,
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
    cookie_uuid = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        db_index=True
    )

class ContactAction(commods.Standard):
    """User contact action.
    
    Last updated: 29 September 2022, 7:07 PM
    """
    contactee = models.ForeignKey(
        'User',
        related_name='contact_actions_as_contactees',
        related_query_name='contact_actions_as_contactees',
        on_delete=models.PROTECT,
        db_index=True
    )
    contactor = models.ForeignKey(
        'User',
        related_name='contact_actions_as_contactor',
        related_query_name='contact_actions_as_contactor',
        on_delete=models.PROTECT,
        db_index=True
    )

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
    reviewee = models.ForeignKey(
        'User',
        related_name='reviews_as_reviewee',
        related_query_name='reviews_as_reviewee',
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

class ReviewImage(commods.Standard):
    """Review image

    Last updated: 29 September 2022, 7:01 PM
    """
    review = models.ForeignKey(
        'Review',
        related_name='images',
        related_query_name='images',
        on_delete=models.PROTECT,
        db_index=True
    )
    file = models.ForeignKey(
        'files.File',
        related_name='reviews_as_image',
        related_query_name='reviews_as_image',
        on_delete=models.PROTECT,
        db_index=True
    )

class ReviewComment(commods.Standard):
    """Review comment

    Last updated: 29 September 2022, 7:01 PM
    """
    review = models.ForeignKey(
        'User',
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

class ReviewCommentImage(commods.Standard):
    """Review comment image

    Last updated: 29 September 2022, 7:01 PM
    """
    comment = models.ForeignKey(
        'ReviewComment',
        related_name='images_as_review_comment',
        related_query_name='images_as_review_comment',
        on_delete=models.PROTECT,
        db_index=True
    )
    file = models.ForeignKey(
        'files.File',
        related_name='review_response_images_as_file',
        related_query_name='review_response_images_as_file',
        on_delete=models.PROTECT,
        db_index=True
    )






















# avatar = models.ForeignKey(
#     'files.File',
#     related_name='avatar_for_users',
#     related_query_name='avatar_for_users',
#     on_delete=models.PROTECT,
#     null=True,
#     blank=True,
#     db_index=True
# )

# def avatar_url(self):
#     path = settings.AWS_S3_KEY_AVATAR_IMAGE % (self.id)
#     return urljoin(settings.MEDIA_URL, path)

# def avatar_thumbnail_url(self):
#     path = settings.AWS_S3_KEY_AVATAR_IMAGE_THUMBNAIL % (self.id)
#     return urljoin(settings.MEDIA_URL, path)

# def refresh_slug(self):
#     """Refresh the slug for this user."""
#     first_user = User.objects.all().order_by('-id').first()
#     if first_user is None:
#         this_id = 0
#     elif self.id is None:
#         # Compute ID because it's not been set.
#         # Collison due to race condition is possible but VERY unlikely.
#         this_id = User.objects.all().order_by('-id').first().id + 1
#     else:
#         this_id = self.id

#     # Create slug out of user's first/last name and company name   
#     self.slug_tokens = f'{self.first_name} {self.last_name}'
#     if self.company_name is not None and len(self.company_name) > 0:
#         self.slug_tokens = f'{self.slug_tokens} {self.company_name}'
#     self.slug_tokens += f' {this_id}'
#     self.slug_link = slugify(self.slug_tokens)

# def save(self, *args, **kwargs):
#     self.refresh_slug()
#     return super().save(*args, **kwargs)

# Alert

# class Alert(commods.Standard):
#     """Alert.

#     Last updated: 13 September 2022, 7:59 PM
#     """
#     user = models.ForeignKey(
#         'User',
#         related_name='user_alerts',
#         related_query_name='user_alerts',
#         on_delete=models.PROTECT,
#         db_index=True
#     )
    
#     key_phrases = models.TextField()
#     is_buying = models.BooleanField(db_index=True)
#     is_selling = models.BooleanField(db_index=True)
#     is_need_commission_agents = models.BooleanField(db_index=True)
#     is_commission_agent = models.BooleanField(db_index=True)
#     is_other = models.BooleanField(db_index=True)

# class AlertMatch(commods.Standard):
#     """Matching alert to user requirements.

#     Last updated: 13 September 2022, 7:59 PM
#     """
#     alert = models.ForeignKey(
#         'Alert',
#         related_name='alert_match_alerts',
#         related_query_name='alert_match_alerts',
#         on_delete=models.PROTECT,
#         db_index=True
#     )
#     requirement = models.ForeignKey(
#         'Requirement',
#         related_name='alert_match_requirements',
#         related_query_name='alert_match_requirements',
#         on_delete=models.PROTECT,
#         db_index=True
#     )
#     status = models.CharField(
#         max_length=20,
#         choices=[
#             ('match', 'Match'),
#             ('not_match', 'Not Match'),
#             ('failed', 'Failed'),
#             ('notified', 'Notified')
#         ],
#         null=True,
#         blank=True,
#         db_index=True
#     )

# class KeyPhrase(commods.Standard):
#     """Unique key phrase used in alerts.

#     Last updated: 13 September 2022, 7:59 PM
#     """
#     key_phrase = models.CharField(
#         max_length=40,
#         db_index=True
#     )

# class AlertKeyPhrase(models.Model):
#     """Key phrase used in an alert.

#     Last updated: 13 September 2022, 7:59 PM
#     """
#     alert = models.ForeignKey(
#         'Alert',
#         related_name='alert_key_phrases',
#         related_query_name='alert_key_phrases',
#         on_delete=models.PROTECT,
#         db_index=True
#     )
#     key_phrase = models.ForeignKey(
#         'KeyPhrase',
#         related_name='alert_key_phrases',
#         related_query_name='alert_key_phrases',
#         on_delete=models.PROTECT,
#         db_index=True
#     )

# class AlertExcludeCountry(models.Model):
#     """Country to exclude from an alert.

#     Last updated: 13 September 2022, 7:59 PM
#     """
#     alert = models.ForeignKey(
#         'Alert',
#         related_name='alert_exclude_countries',
#         related_query_name='alert_exclude_countries',
#         on_delete=models.PROTECT,
#         db_index=True
#     )
#     country = models.ForeignKey(
#         'common.Country',
#         related_name='alert_exclude_countries',
#         related_query_name='alert_exclude_countries',
#         on_delete=models.PROTECT,
#         db_index=True
#     )

# from django.db.models import Q
# import leads.models as lemods

# class MagicLinkRedirect(commods.Standard):
#     """Magic link redirect.

#     Last updated: 20 July 2022, 2:59 PM
#     """
#     user = models.ForeignKey(
#         'relationships.User',
#         related_name='magic_link_redirects',
#         related_query_name='magic_link_redirects',
#         on_delete=models.PROTECT,
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     uuid = models.CharField(
#         max_length=100,
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     next = models.CharField(
#         max_length=200,
#         null=True,
#         blank=True,
#         db_index=True
#     )

# class UserComment(commods.Standard):
#     """Comment on a user

#     Last updated: 14 February 2022, 11:33 AM
#     """
#     commentee = models.ForeignKey(
#         'User',
#         related_name='user_comments_as_commentee',
#         related_query_name='user_comments_as_commentee',
#         on_delete=models.PROTECT,
#         db_index=True
#     )
#     commentor = models.ForeignKey(
#         'User',
#         related_name='user_comments_as_commentor',
#         related_query_name='user_comments_as_commentor',
#         on_delete=models.PROTECT,
#         db_index=True
#     )

#     body = models.TextField()

#     reply_to = models.ForeignKey(
#         'UserComment',
#         related_name='replies',
#         related_query_name='replies',
#         on_delete=models.PROTECT,
#         null=True,
#         blank=True,
#         db_index=True
#     )

#     def reply_comments(self):
#         """Returns replies to this lead"""
#         return UserComment.objects.filter(
#             reply_to=self,
#             deleted__isnull=True
#         ).order_by('created')

# class SavedUser(commods.Standard):
#     """Saved user.

#     Last updated: 28 February 2022, 3:58 PM
#     """
#     active = models.BooleanField(
#         default=True,
#         db_index=True
#     )
#     saver = models.ForeignKey(
#         'User',
#         related_name='saved_users_saver',
#         related_query_name='saved_users_saver',
#         on_delete=models.PROTECT,
#         db_index=True        
#     )
#     savee = models.ForeignKey(
#         'User',
#         related_name='saved_users_savee',
#         related_query_name='saved_users_savee',
#         on_delete=models.PROTECT,
#         db_index=True  
#     )

#     class Meta:
#         unique_together = ('saver', 'savee')

# class UserQuery(commods.Standard):
#     """User query

#     Last updated: 15 March 2022, 3:59 AM
#     """
#     user = models.ForeignKey(
#         'User',
#         related_name='user_queries',
#         related_query_name='user_queries',
#         on_delete=models.PROTECT,
#         db_index=True        
#     )

#     commented_only = models.CharField(
#         max_length=200,
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     saved_only = models.CharField(
#         max_length=200,
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     connected_only = models.CharField(
#         max_length=200,
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     first_name = models.CharField(
#         max_length=200,
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     last_name = models.CharField(
#         max_length=200,
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     company_name = models.CharField(
#         max_length=200,
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     country = models.CharField(
#         max_length=200,
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     goods_string = models.CharField(
#         max_length=200,
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     languages = models.CharField(
#         max_length=200,
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     is_buy_agent = models.CharField(
#         max_length=200,
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     buy_agent_details = models.CharField(
#         max_length=200,
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     is_sell_agent = models.CharField(
#         max_length=200,
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     sell_agent_details = models.CharField(
#         max_length=200,
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     is_logistics_agent = models.CharField(
#         max_length=200,
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     logistics_agent_details = models.CharField(
#         max_length=200,
#         null=True,
#         blank=True,
#         db_index=True
#     )

# class LoginToken(commods.Standard):
#     """Login token.
    
#     Last updated: 15 February 2022, 3:46 PM
#     """
#     user = models.ForeignKey(
#         'User',
#         related_name='login_tokens',
#         related_query_name='login_tokens',
#         on_delete=models.PROTECT,
#         db_index=True
#     )
#     is_not_latest = models.BooleanField(
#         db_index=True,
#         null=True,
#         blank=True
#     )
#     activated = models.DateTimeField(
#         db_index=True,
#         null=True,
#         blank=True
#     )
#     killed = models.DateTimeField(
#         db_index=True,
#         null=True,
#         blank=True
#     )
#     token = models.CharField(
#         unique=True,
#         max_length=200,
#         db_index=True,
#         default=get_token
#     )

# class RegisterToken(commods.Standard):
#     """Register token.
    
#     Last updated: 15 February 2022, 3:46 PM
#     """
#     token = models.CharField(
#         unique=True,
#         max_length=200,
#         db_index=True,
#         default=get_token
#     )
#     user = models.ForeignKey(
#         'User',
#         related_name='register_tokens',
#         related_query_name='register_tokens',
#         on_delete=models.PROTECT,
#         db_index=True
#     )
#     is_not_latest = models.BooleanField(
#         db_index=True,
#         null=True,
#         blank=True
#     )
#     activated = models.DateTimeField(
#         db_index=True,
#         null=True,
#         blank=True
#     )
#     killed = models.DateTimeField(
#         db_index=True,
#         null=True,
#         blank=True
#     )

# Not in Use

# def num_leads(self):
#     return lemods.Lead.objects.filter(author=self.id).count()

# def num_contacts(self):
#     if self.email is None and self.phone_number is None:
#         return 0

#     q = Q()
#     if self.email is not None:
#         q = q | Q(email=self.email)

#     if self.phone_number is not None:
#         q = q | Q(phone_number=self.phone_number)

#     return lemods.Contact.objects.filter(q).count()

# def num_whatsapped(self):
#     return lemods.ContactAction.objects.filter(
#         contact__lead__author=self,
#         type='whatsapp',
#         deleted__isnull=True
#     ).count()

# def num_wechatted(self):
#     return lemods.ContactAction.objects.filter(
#         contact__lead__author=self,
#         type='wechat',
#         deleted__isnull=True
#     ).count()

# def num_private_notes(self):
#     return lemods.ContactNote.objects.filter(
#         contact__lead__author=self,
#         deleted__isnull=True
#     ).count()

# def leads_order_by_created_desc(self):
#     return lemods.Lead.objects.filter(
#         author=self.id,
#         deleted__isnull=True
#     ).order_by('-created')

# def is_country_match_country_code(self):
#     if self.phone_number is not None and self.country is not None:
#         return self.country.country_code == self.phone_number.country_code

#     return False

# Not in use

# def country_from_phone_number(self):
#     """Returns country from user's phone number country code."""
#     try:
#         return commods.Country.objects.get(
#             country_code=self.phone_number.country_code)
#     except commods.Country.DoesNotExist:
#         return None

# def is_profile_complete(self):
#     """Returns True if profile is complete."""
#     return self.first_name != None and \
#         self.last_name != None and \
#         self.phone_number != None and \
#         self.country != None

# def applications(self):
#     """Returns applications associated with this user."""

#     # Applications where this user is the applicant and lead author has replied
#     applications = lemods.Application.objects.filter(
#         applicant=self,
#         last_messaged__isnull=False
#     )

#     # Applications where this user is the product owner
#     for lead in lemods.Lead.objects.filter(author=self.id):
#         # Merge all applications
#         applications = applications | lead.applications.all()

#     applications = applications.filter(deleted__isnull=True)

#     # Sort by last messaged date/time
#     applications = applications.order_by('-last_messaged')

#     return applications

# def root_comments(self):
#     """Returns root comments only (i.e., comments that are not replies to
#     a comment. We do not chain replies and all replies are to root comments.
#     """
#     return UserComment.objects.filter(
#         commentee=self,
#         reply_to__isnull=True
#     ).order_by('created')

# def num_comments_as_commentee(self):
#     return UserComment.objects.filter(commentee=self).count()

# def num_credits_left(self):
#     sum = paymods.CreditsEvent.objects.filter(user=self)\
#         .aggregate(models.Sum('value'))

#     if sum['value__sum'] is None:
#         return 0

#     return sum['value__sum']

# def seo_title(self):
#     """Returns SEO-optimized title"""

#     title = 'Import/Export'
#     if self.is_buy_agent or self.is_sell_agent or self.is_logistics_agent:
#         if self.is_buy_agent:
#             title += ', Buying Agent'
#         if self.is_sell_agent:
#             title += ', Selling Agent'
#         if self.is_logistics_agent:
#             title += ', Logistics Agent'

#     if self.slug_tokens is not None and len(self.slug_tokens.strip()) != 0:
#         tokens = self.slug_tokens.split(',')
#         tokens = [t.strip() for t in tokens]
#         if len(tokens) > 0:
#             keywords = tokens[0]
#             for t in tokens[1:]:
#                 if len(keywords) < 40:
#                     keywords += ' ' + t
            
#             title += ' - ' + keywords

#     return title