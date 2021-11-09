from django.db import models
from common.models import Standard
import uuid

class File(Standard):
    """File in S3
    
    Last updated: 9 November 2021 11:32
    """
    
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )
    uploader = models.ForeignKey(
        'relationships.User',
        related_name='uploaded_files',
        related_query_name='uploaded_files',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_index=True
    )
    file_type = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True
    )
    presigned_url_issued = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True
    )
    presigned_url_lifespan = models.IntegerField(
        null=True,
        blank=True,
        db_index=True
    )
    presigned_url_response = models.JSONField(
        null=True,
        blank=True
    )
    lifespan = models.IntegerField(
        null=True,
        blank=True,
        db_index=True
    )

    s3_bucket_name = models.CharField(
        max_length=63,
        null=True,
        blank=True,
        db_index=True
    )
    s3_object_key = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
        db_index=True
    )
    s3_object_content_length = models.PositiveIntegerField(
        null=True, 
        blank=True,
        db_index=True
    )
    s3_object_e_tag = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    s3_object_content_type = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True
    )
    s3_object_last_modified = models.DateTimeField(
        default=None,
        null=True,
        blank=True,
        db_index=True
    )

    def __str__(self):
        return f'({self.s3_bucket_name}, {self.s3_object_key} [{self.id}])'

    class Meta:
        unique_together = ('s3_bucket_name', 's3_object_key')