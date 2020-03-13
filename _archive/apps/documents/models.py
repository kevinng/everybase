from django.contrib.postgres.fields import JSONField
from django.db import models
import uuid

from accounts.models import Account, Organization
from materials.models import Material, Batch

class DocumentType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    acronym = models.CharField(max_length=10)
    level = models.CharField(max_length=20, choices=[
        ('material', 'Material-Level'),
        ('batch', 'Batch-Level')
    ], default='material')

    def __str__(self):
        # User-facing text
        return self.name + ' (' + self.acronym + ')'

    class Meta:
        verbose_name = 'Document Type'
        verbose_name_plural = 'Document Types'

class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, default=None)

    creator = models.ForeignKey(Account,
        models.CASCADE, related_name='created_documents')
    document_type = models.ForeignKey(DocumentType,
        models.CASCADE, related_name='documents')
    organization = models.ForeignKey(Organization,
        models.CASCADE, related_name='documents')
    batch = models.ForeignKey(Batch,
        models.CASCADE,
        null=True, default=None,
        related_name='documents')
    material = models.ForeignKey(Material,
        models.CASCADE,
        related_name='documents')

    def __str__(self):
        string = 'ID: %s, Created: %s, Material: %s' % (
            str(self.id)[:4],
            self.created.strftime("%b %d %Y %H:%M:%S"),
            self.material.name
        )

        if self.batch != None:
            string += ', Batch: ' + self.batch.code

        if self.deleted != None:
            string += ' [Deleted]'

        return string

class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    saved = models.DateTimeField(null=True, default=None)
    deleted = models.DateTimeField(null=True, default=None)
    presigned_url_issued = models.DateTimeField(auto_now_add=True)
    presigned_url_lifespan = models.IntegerField()
    presigned_url_response = JSONField()
    filetype = models.CharField(max_length=100)
    s3_bucket_name = models.CharField(max_length=63)
    s3_object_key = models.CharField(max_length=1024)

    document = models.ForeignKey(Document,
        models.CASCADE,
        null=True, default=None,
        related_name='files')
    creator = models.ForeignKey(Account,
        models.CASCADE,
        related_name='files_uploaded')

    def __str__(self):
        return 'Saved: %s, Key: %s' % (self.saved, self.s3_object_key)

    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'