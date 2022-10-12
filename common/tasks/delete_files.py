import boto3
from celery import shared_task
from everybase import settings

@shared_task
def delete_files(delete_objs):
    """Delete files specified in delete_objs list in the format:
    [
        {'Key': <AWS S3 key>}
        ...
    ]
    """
    bucket = boto3.session.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    ).resource('s3').Bucket(settings.AWS_STORAGE_BUCKET_NAME)

    bucket.delete_objects(Delete={'Objects': delete_objs})
    