import requests, os, boto3, sentry_sdk, pytz, datetime
from everybase.settings import (CHAT_FILE_TRANSFER_CACHE_PATH,
    AWS_STORAGE_BUCKET_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY,
    TIME_ZONE)
from celery import shared_task
from relationships import models as relmods
from files import models as filemods

@shared_task
def save_lead_media(
        lead_id: int,
        content_type: str,
        url: str,
        no_external_calls: bool = False
    ) -> relmods.Lead:
    """Save media for a lead to S3.

    Parameters
    ----------
    lead_id
        ID of the lead we're saving the media for
    content_type
        Content type of the media
    url
        Unprotected media URL - e.g., from Twilio
    no_external_calls
        If True, will not make external API calls - e.g., send Twilio WhatsApp
        messages. Useful for automated testing, to ascertain model updates are
        made correctly.
    """
    # Create file model row and associate it with lead
    
    lead = relmods.Lead.objects.get(pk=lead_id)
    file = filemods.File.objects.create(
        lead=lead,
        s3_bucket_name=AWS_STORAGE_BUCKET_NAME,
        s3_object_content_type=content_type
    )
    filename = file.uuid
    s3_object_key = f'chat/leads/{lead_id}/medias/{filename}'
    file.s3_object_key=s3_object_key

    # Cache file locally
    r = requests.get(url, allow_redirects=True)
    local_path = os.path.join(CHAT_FILE_TRANSFER_CACHE_PATH, filename)
    open(local_path, 'wb').write(r.content)

    # Upload to S3
    if no_external_calls == False:
        s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        try:
            s3.upload_file(
                local_path,
                AWS_STORAGE_BUCKET_NAME,
                s3_object_key,
                ExtraArgs={'ContentType': content_type}
            )
        except Exception as e:
            sentry_sdk.capture_exception(e)
            return None

    # Delete local cached copy
    os.remove(local_path)

    # Set file upload confirmed timestamp.
    sgtz = pytz.timezone(TIME_ZONE)
    file.upload_confirmed = datetime.datetime.now(tz=sgtz)

    # Save file
    file.save()

    return lead