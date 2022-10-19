import boto3
from celery import shared_task
from everybase import settings
from relationships import models

@shared_task
def delete_review_file(
        user_id: int,
        file_uuid: int,
        form_uuid: str,
    ):
    """Delete specific file."""
    bucket = boto3.session.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    ).resource('s3').Bucket(settings.AWS_STORAGE_BUCKET_NAME)

    reviewer = models.User.objects.get(pk=user_id)

    bucket = boto3.session.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    ).resource('s3').Bucket(settings.AWS_STORAGE_BUCKET_NAME)

    file = models.ReviewFile.objects.filter(
        reviewer=reviewer,
        file_uuid=file_uuid,
        form_uuid=form_uuid
    ).first()

    if file is not None:
        file.delete()
        delete_objs = []
        delete_objs.append({'Key': file.file.s3_object_key})
        delete_objs.append({'Key': file.file.thumbnail_s3_object_key})
        bucket.delete_objects(Delete={'Objects': delete_objs})