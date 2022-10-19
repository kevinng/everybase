import boto3
from celery import shared_task
from everybase import settings
from relationships import models

@shared_task
def clear_abandoned_files(
        user_id: int,
        form_uuid: str=None,
        activated: bool=True
    ):
    """Delete status and review files from this user that's from abandoned
    forms. Files in use are identified by their activated timestamps and files
    from other forms have a different form_uuid from the one specified."""
    bucket = boto3.session.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    ).resource('s3').Bucket(settings.AWS_STORAGE_BUCKET_NAME)

    user = models.User.objects.get(pk=user_id)

    # Form UUID should be unique across all tables.

    status_files = models.StatusFile.objects\
        .filter(user=user)\
        .filter(activated__isnull=not activated)\
        .exclude(form_uuid=form_uuid)

    review_files = models.ReviewFile.objects\
        .filter(user=user)\
        .filter(activated__isnull=not activated)\
        .exclude(form_uuid=form_uuid)

    review_comment_files = models.ReviewCommentFile.objects\
        .filter(comment__author=user)\
        .filter(activated__isnull=not activated)\
        .exclude(form_uuid=form_uuid)

    delete_objs = []

    for sf in status_files:
        file = sf.file
        delete_objs.append({'Key': file.s3_object_key})
        delete_objs.append({'Key': file.thumbnail_s3_object_key})
        sf.delete()
        file.delete()

    for rf in review_files:
        file = rf.file
        delete_objs.append({'Key': file.s3_object_key})
        delete_objs.append({'Key': file.thumbnail_s3_object_key})
        rf.delete()
        file.delete()

    for rcf in review_comment_files:
        file = rcf.file
        delete_objs.append({'Key': file.s3_object_key})
        delete_objs.append({'Key': file.thumbnail_s3_object_key})
        rcf.delete()
        file.delete()
    
    # Delete orphan files if any.
    if len(delete_objs) > 0:
        bucket.delete_objects(Delete={'Objects': delete_objs})