import random, uuid

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User as django_user
from django.utils.text import slugify

from common import models as commods
import leads.models as lemods

class PhoneNumberType(commods.Choice):
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
        return f'(+{self.country_code} {self.national_number}, [{self.id}])'

    class Meta:
        unique_together = ['country_code', 'national_number']

class Email(commods.Standard):
    """Email.

    Last updated: 15 October 2021, 11:05 PM
    """

    verified = models.DateTimeField(
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

    def __str__(self):
        return f'({self.email} [{self.id}])'

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
        return f'({self.email} [{self.id}])'

class User(commods.Standard):
    """User details.

    Last updated: 5 May 2022, 1:13 PM
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

    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False,
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
        related_name='users_w_this_country',
        related_query_name='users_w_this_country',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )

    slug_link = models.CharField(
        max_length=200,
        unique=True,
        db_index=True
    )
    slug_tokens = models.TextField(
        null=True,
        blank=True
    )

    internal_notes = models.TextField(
        null=True,
        blank=True
    )

    # Not in Use

    impressions = models.IntegerField(
        default=1, # Prevent division by 0
        db_index=True
    )
    clicks = models.IntegerField(
        default=0,
        db_index=True
    )

    has_company = models.BooleanField(
        null=True,
        blank=True,
        db_index=True
    )
    company_name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        db_index=True
    )
    goods_string = models.TextField(
        null=True,
        blank=True
    )
    buy_agent_details = models.TextField(
        null=True,
        blank=True
    )
    sell_agent_details = models.TextField(
        null=True,
        blank=True
    )
    logistics_agent_details = models.TextField(
        null=True,
        blank=True
    )

    is_buyer = models.BooleanField(
        null=True,
        blank=True,
        db_index=True
    )
    is_seller = models.BooleanField(
        null=True,
        blank=True,
        db_index=True
    )
    is_buy_agent = models.BooleanField(
        null=True,
        blank=True,
        db_index=True
    )
    is_sell_agent = models.BooleanField(
        null=True,
        blank=True,
        db_index=True
    )
    is_logistics_agent = models.BooleanField(
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
    languages = models.ManyToManyField(
        'common.Language',
        related_name='users_w_this_language',
        related_query_name='users_w_this_language',
        blank=True,
        db_index=True
    )
    languages_string = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    def refresh_slug(self):
        """Refresh the slug for this user."""
        first_user = User.objects.all().order_by('-id').first()
        if first_user is None:
            this_id = 0
        elif self.id is None:
            # Compute ID because it's not been set.
            # Collison due to race condition is possible but VERY unlikely.
            this_id = User.objects.all().order_by('-id').first().id + 1
        else:
            this_id = self.id

        # Create slug out of user's first/last name and company name   
        self.slug_tokens = f'{self.first_name} {self.last_name}'
        if self.company_name is not None and len(self.company_name) > 0:
            self.slug_tokens = f'{self.slug_tokens} {self.company_name}'
        self.slug_tokens += f' {this_id}'
        self.slug_link = slugify(self.slug_tokens)

    def save(self, *args, **kwargs):
        # Refresh slug when this user is saved
        self.refresh_slug()
        return super().save(*args, **kwargs)

    def country_from_phone_number(self):
        """Returns country from user's phone number country code."""
        try:
            return commods.Country.objects.get(
                country_code=self.phone_number.country_code)
        except commods.Country.DoesNotExist:
            return None

    def applications(self):
        """Returns applications associated with this user."""

        # Applications where this user is the applicant and lead author has replied
        applications = lemods.Application.objects.filter(
            applicant=self,
            last_messaged__isnull=False
        )

        # Applications where this user is the product owner
        for lead in lemods.Lead.objects.filter(author=self.id):
            # Merge all applications
            applications = applications | lead.applications.all()

        applications = applications.filter(deleted__isnull=True)

        # Sort by last messaged date/time
        applications = applications.order_by('-last_messaged')

        return applications

    def is_profile_complete(self):
        """Returns True if profile is complete."""
        return self.first_name != None and \
            self.last_name != None and \
            self.phone_number != None and \
            self.country != None

    def __str__(self):
        return f'{self.first_name} {self.last_name} [{self.id}]'

    # Not in use

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

    # def num_leads(self):
    #     return lemods.Lead.objects.filter(author=self.id).count()

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







































# Not in use

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
        unique_together = ['user', 'ip_address', 'is_routable', 'is_mobile', 'is_tablet', 'is_touch_capable', 'is_pc',
            'is_bot', 'browser', 'browser_family', 'browser_version', 'browser_version_string', 'os', 'os_family',
            'os_version', 'os_version_string', 'device', 'device_family']

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

class LoginToken(commods.Standard):
    """Login token.
    
    Last updated: 15 February 2022, 3:46 PM
    """
    user = models.ForeignKey(
        'User',
        related_name='login_tokens',
        related_query_name='login_tokens',
        on_delete=models.PROTECT,
        db_index=True
    )
    is_not_latest = models.BooleanField(
        db_index=True,
        null=True,
        blank=True
    )
    activated = models.DateTimeField(
        db_index=True,
        null=True,
        blank=True
    )
    killed = models.DateTimeField(
        db_index=True,
        null=True,
        blank=True
    )
    token = models.CharField(
        unique=True,
        max_length=200,
        db_index=True,
        default=get_token
    )

class RegisterToken(commods.Standard):
    """Register token.
    
    Last updated: 15 February 2022, 3:46 PM
    """
    token = models.CharField(
        unique=True,
        max_length=200,
        db_index=True,
        default=get_token
    )
    user = models.ForeignKey(
        'User',
        related_name='register_tokens',
        related_query_name='register_tokens',
        on_delete=models.PROTECT,
        db_index=True
    )
    is_not_latest = models.BooleanField(
        db_index=True,
        null=True,
        blank=True
    )
    activated = models.DateTimeField(
        db_index=True,
        null=True,
        blank=True
    )
    killed = models.DateTimeField(
        db_index=True,
        null=True,
        blank=True
    )

class UserDetailView(commods.Standard):
    """User detail view
    
    Last updated: 28 February 2022, 12:17 AM
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
        related_name='user_detail_views_with_this_user_as_viewer',
        related_query_name='user_detail_views_with_this_user_as_viewer',
        on_delete=models.PROTECT,
        db_index=True
    )
    
    comments_view_count = models.IntegerField(
        default=0,
        db_index=True    
    )
    leads_view_count = models.IntegerField(
        default=0,
        db_index=True    
    )

class UserComment(commods.Standard):
    """Comment on a user

    Last updated: 14 February 2022, 11:33 AM
    """
    commentee = models.ForeignKey(
        'User',
        related_name='user_comments_as_commentee',
        related_query_name='user_comments_as_commentee',
        on_delete=models.PROTECT,
        db_index=True
    )
    commentor = models.ForeignKey(
        'User',
        related_name='user_comments_as_commentor',
        related_query_name='user_comments_as_commentor',
        on_delete=models.PROTECT,
        db_index=True
    )

    body = models.TextField()

    reply_to = models.ForeignKey(
        'UserComment',
        related_name='replies',
        related_query_name='replies',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_index=True
    )

    def reply_comments(self):
        """Returns replies to this lead"""
        return UserComment.objects.filter(
            reply_to=self,
            deleted__isnull=True
        ).order_by('created')

class SavedUser(commods.Standard):
    """Saved user.

    Last updated: 28 February 2022, 3:58 PM
    """
    active = models.BooleanField(
        default=True,
        db_index=True
    )
    saver = models.ForeignKey(
        'User',
        related_name='saved_users_saver',
        related_query_name='saved_users_saver',
        on_delete=models.PROTECT,
        db_index=True        
    )
    savee = models.ForeignKey(
        'User',
        related_name='saved_users_savee',
        related_query_name='saved_users_savee',
        on_delete=models.PROTECT,
        db_index=True  
    )

    class Meta:
        unique_together = ('saver', 'savee')

class UserQuery(commods.Standard):
    """User query

    Last updated: 15 March 2022, 3:59 AM
    """
    user = models.ForeignKey(
        'User',
        related_name='user_queries',
        related_query_name='user_queries',
        on_delete=models.PROTECT,
        db_index=True        
    )

    commented_only = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    saved_only = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    connected_only = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    first_name = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    last_name = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    company_name = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    country = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    goods_string = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    languages = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    is_buy_agent = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    buy_agent_details = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    is_sell_agent = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    sell_agent_details = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    is_logistics_agent = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    logistics_agent_details = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )