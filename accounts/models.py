from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid, datetime

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