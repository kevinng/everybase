import boto3
from celery import shared_task
from everybase import settings
from relationships import models

@shared_task
def upload_status_files__delete_other_files(
        user_id: int,
        form_uuid: str=None
    ):
    """Delete files from this user that's from abandoned forms. User may already
    have files in use. Files in use are identified by their activated timestamps
    and files from other forms have a different form_uuid from the one
    specified."""
    bucket = boto3.session.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    ).resource('s3').Bucket(settings.AWS_STORAGE_BUCKET_NAME)

    user = models.User.objects.get(pk=user_id)

    # Not in use and not from this form.
    status_files = models.StatusFile.objects\
        .filter(user=user)\
        .filter(activated__isnull=True)\
        .exclude(form_uuid=form_uuid)

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