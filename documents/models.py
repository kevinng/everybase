from django.db import models
import uuid

from accounts.models import Account, Organization
from materials.models import Material, Batch

class DocumentType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    acronym = models.CharField(max_length=10)

    def __str__(self):
        return self.name + ' (' + self.acronym + ')'

    class Meta:
        verbose_name = 'Document Type'
        verbose_name_plural = 'Document Types'

class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True)

    creator = models.ForeignKey(Account,
        models.CASCADE, related_name='created_documents')
    document_type = models.ForeignKey(DocumentType,
        models.CASCADE, related_name='documents')
    organization = models.ForeignKey(Organization,
        models.CASCADE, related_name='documents')
    batches = models.ManyToManyField(Batch,
        through='DocumentBatch', related_name='documents')
    materials = models.ManyToManyField(Material,
        through='DocumentMaterial', related_name='documents')

class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True)
    s3_bucket_region = models.CharField(max_length=20)
    s3_bucket_name = models.CharField(max_length=63)
    s3_bucket_arn = models.CharField(max_length=2024)
    s3_object_key = models.CharField(max_length=1024)
    s3_object_content_length = models.IntegerField()
    s3_object_e_tag = models.CharField(max_length=1024)
    s3_object_content_type = models.CharField(max_length=30)
    s3_object_last_modified = models.DateTimeField()

    document = models.ForeignKey(Document,
        models.CASCADE, related_name='files')

class DocumentMaterial(models.Model):
    document = models.ForeignKey(Document, models.CASCADE)
    material = models.ForeignKey(Material, models.CASCADE)

    class Meta:
        verbose_name = 'Document-Material'
        verbose_name_plural = 'Document-Materials'

class DocumentBatch(models.Model):
    document = models.ForeignKey(Document, models.CASCADE)
    batch = models.ForeignKey(Batch, models.CASCADE)

    class Meta:
        verbose_name = 'Document-Batch'
        verbose_name_plural = 'Document-Batches'