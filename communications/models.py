from django.db import models
import uuid

from accounts.models import Account, Organization
from documents.models import Document

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sent = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    comments = models.TextField()
    
    sender = models.ForeignKey(Account,
        models.CASCADE, related_name='sent_messages')
    organization = models.ForeignKey(Organization,
        models.CASCADE, related_name='messages')
    documents = models.ManyToManyField(Document, related_name='messages')
    recipient_accounts = models.ManyToManyField(Account,
        through='Recipient', related_name='received_messages')

class Recipient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()

    message = models.ForeignKey(Message,
        models.CASCADE, related_name='recipients')
    organization = models.ForeignKey(Organization,
        models.CASCADE, related_name='recipients')
    account = models.ForeignKey(Account, models.CASCADE,
        blank=True, null=True, default=None, related_name='recipients')