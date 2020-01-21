from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid, datetime

class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        return self.name
    
class Account(models.Model):
    id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(blank=True, null=True, default=None)

    user = models.OneToOneField(User, models.CASCADE, primary_key=True)
    active_organization = models.ForeignKey(Organization, models.CASCADE,
        blank=True, null=True, default=None, related_name='active_accounts')
    organizations = models.ManyToManyField(Organization,
        through='AccountOrganization', related_name='accounts')
    
    def __str__(self):
        return self.user.email

class AccountOrganization(models.Model):
    role = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(blank=True, null=True, default=None)

    account = models.ForeignKey(Account, models.CASCADE)
    organization = models.ForeignKey(Organization, models.CASCADE)

    class Meta:
        verbose_name = 'Account-Organization'
        verbose_name_plural = 'Account-Organizations'

    def __str__(self):
        return '%s, %s, %s' % (self.account, self.organization, self.role)

class EmailVerificationCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()
    verified = models.DateTimeField(
        blank=True, null=True, default=None)
    ip_address = models.GenericIPAddressField('IP Address',
        blank=True, null=True, default=None)

    class Meta:
        ordering = ["created"]

    def is_expired(self):
        return timezone.now() - datetime.timedelta(hours=24) > self.created

    def is_valid(self):
        return not self.is_expired() and not self.verified == None

    def is_old_enough(self):
        return timezone.now() - datetime.timedelta(minutes=5) > self.created

    class Meta:
        verbose_name = 'Email Verification Code'
        verbose_name_plural = 'Email Verification Codes'

class PasswordResetCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    account = models.ForeignKey(Account, models.CASCADE, null=True,
        related_name='requested_password_reset_codes')

    class Meta:
        ordering = ["created"]
        verbose_name = 'Password Reset Code'
        verbose_name_plural = 'Password Reset Codes'

    def is_expired(self):
        return timezone.now() - datetime.timedelta(hours=24) > self.created

    def is_valid(self):
        return not self.is_expired() and not self.used

    def is_old_enough(self):
        return timezone.now() - datetime.timedelta(minutes=5) > self.created

    def __str__(self):
        return self.account.user.email
    
class OrganizationInvitationCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()
    used = models.BooleanField(default=False)

    recipient = models.ForeignKey(Account, models.CASCADE,
        blank=True, null=True, default=None,
        related_name='received_organization_invitation_codes')
    requestor = models.ForeignKey(Account, models.CASCADE,
        related_name='created_organization_invitation_codes')
    organization = models.ForeignKey(Account, models.CASCADE,
        related_name='invitation_codes')

    class Meta:
        ordering = ["created"]
        verbose_name = 'Organization Invitation Code'
        verbose_name_plural = 'Organization Invitation Codes'

    def is_expired(self):
        return timezone.now() - datetime.timedelta(hours=24) > self.created

    def is_valid(self):
        return not self.is_expired() and not self.used

    def is_old_enough(self):
        return timezone.now() - datetime.timedelta(minutes=5) > self.created