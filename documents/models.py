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
        return self.name + ' (' + self.acronym + ')'

    class Meta:
        verbose_name = 'Document Type'
        verbose_name_plural = 'Document Types'

class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(blank=True, null=True, default=None)

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
    presigned_url_issued = models.DateTimeField(auto_now_add=True)
    file_uploaded = models.DateTimeField(blank=True, null=True, default=None)
    deleted = models.DateTimeField(blank=True, null=True, default=None)
    presigned_url = models.URLField()
    expires_in = models.IntegerField()
    bucket_name = models.CharField(max_length=63)
    object_key = models.CharField(max_length=1024)
    object_content_length = models.IntegerField(blank=True, null=True, default=None)
    object_e_tag = models.CharField(blank=True, null=True, default=None, max_length=1024)
    object_content_type = models.CharField(blank=True, null=True, default=None, max_length=30)
    object_last_modified = models.DateTimeField(blank=True, null=True, default=None)

    uploader = models.ForeignKey(Document,
        blank=True, null=True, default=None,
        models.CASCADE, related_name='files_uploaded')
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