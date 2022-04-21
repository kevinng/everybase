import datetime, pytz, boto3
from files import models as fimods
from everybase import settings

def delete_file(file_id):
    file = fimods.File.objects.get(pk=file_id)

    # Mark file as deleted
    sgtz = pytz.timezone(settings.TIME_ZONE)
    now = datetime.datetime.now(tz=sgtz)
    file.deleted = now
    file.save()

    s3 = boto3.session.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    ).resource('s3')

    # Delete file
    s3.Object(file.s3_bucket_name, file.s3_object_key).delete()

    # Delete thumbnail if any
    if (file.thumbnail_s3_bucket_name is not None and \
        file.thumbnail_s3_object_key):
        s3.Object(
            file.thumbnail_s3_bucket_name,
            file.thumbnail_s3_object_key)\
            .delete()