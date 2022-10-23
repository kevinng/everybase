import boto3
from celery import shared_task
from everybase import settings

@shared_task
def delete_objs(objs):
    """Delete S3 objects."""
    bucket = boto3.session.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    ).resource('s3').Bucket(settings.AWS_STORAGE_BUCKET_NAME)

    if len(objs) > 0:
        bucket.delete_objects(Delete={'Objects': objs})