from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid, datetime

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    role = models.CharField(max_length=100)
    verified_email = models.BooleanField(default=False)
    accepted_terms = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True)

    def __str__(self):
        return self.user.email

class EmailVerificationCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    email = models.CharField(max_length=254)
    used = models.BooleanField(default=False)

    class Meta:
        ordering = ["created"]

    def is_expired(self):
        return timezone.now() - datetime.timedelta(hours=24) > self.created

    def is_valid(self):
        return not self.is_expired() and not self.used

    def is_old_enough(self):
        return timezone.now() - datetime.timedelta(minutes=5) > self.created

class PasswordResetCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, models.SET_NULL, null=True)
    used = models.BooleanField(default=False)

    class Meta:
        ordering = ["created"]

    def is_expired(self):
        return timezone.now() - datetime.timedelta(hours=24) > self.created

    def is_valid(self):
        return not self.is_expired() and not self.used

    def is_old_enough(self):
        return timezone.now() - datetime.timedelta(minutes=5) > self.created