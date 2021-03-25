from django.db import models
from common.models import Standard, Choice
import uuid

class File(Standard):
    upload_confirmed = models.DateTimeField(
        default=None,
        null=True,
        blank=True,
        db_index=True
    )
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False,
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