import boto3
from celery import shared_task
from everybase import settings
from relationships import models

@shared_task
def delete_orphan_files(user_id: int):
    """Delete files that were uploaded and abandoned by a user."""
    bucket = boto3.session.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    ).resource('s3').Bucket(settings.AWS_STORAGE_BUCKET_NAME)

    user = models.User.objects.get(pk=user_id)

    status_files = models.StatusFile.objects\
        .filter(user=user, activated__isnull=True)

    delete_objs = []

    for sf in status_files:
        file = sf.file
        delete_objs.append({'Key': file.s3_object_key})
        delete_objs.append({'Key': file.thumbnail_s3_object_key})
        sf.delete()
        file.delete()
    
    # Delete orphan files if any.
    if len(delete_objs) > 0:
        bucket.delete_objects(Delete={'Objects': delete_objs})