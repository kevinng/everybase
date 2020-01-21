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

class CreateFilePresignedURL(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    issued = models.DateTimeField(auto_now_add=True)
    lifespan = models.IntegerField()
    response = JSONField()
    filetype = models.CharField(max_length=100)
    s3_bucket_name = models.CharField(max_length=63)
    s3_object_key = models.CharField(max_length=1024)

    requester = models.ForeignKey(Account,
        models.CASCADE,
        related_name='requested_create_file_presigned_urls')

    def __str__(self):
        return self.issued.strftime("%d %B %Y, %H:%M:%S %z")

    class Meta:
        verbose_name = 'Create-File-Presigned-URL'
        verbose_name_plural = 'Create-File-Presigned-URLs'

class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uploaded = models.DateTimeField(auto_now_add=True)
    deleted = models.DateTimeField(blank=True, null=True, default=None)
    s3_bucket_name = models.CharField(max_length=63)
    s3_object_key = models.CharField(max_length=1024)
    s3_object_content_length = models.IntegerField(blank=True, null=True, default=None)
    s3_object_e_tag = models.CharField(blank=True, null=True, default=None, max_length=1024)
    s3_object_content_type = models.CharField(blank=True, null=True, default=None, max_length=30)
    s3_object_last_modified = models.DateTimeField(blank=True, null=True, default=None)

    document = models.ForeignKey(Document,
        models.CASCADE,
        blank=True, null=True, default=None,
        related_name='files')
    uploader = models.ForeignKey(Account,
        models.CASCADE,
        related_name='files_uploaded')
    create_presigned_url = models.OneToOneField(CreateFilePresignedURL,
        models.CASCADE,
        related_name='file')

class ReadFilePresignedURL(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    issued = models.DateTimeField(auto_now_add=True)
    lifespan = models.IntegerField()

    requester = models.ForeignKey(Account,
        models.CASCADE,
        related_name='requested_read_file_presigned_urls')
    file = models.ForeignKey(File,
        models.CASCADE,
        related_name='read_presigned_urls')

    class Meta:
        verbose_name = 'Read-File-Presigned-URL'
        verbose_name_plural = 'Read-File-Presigned-URLs'

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