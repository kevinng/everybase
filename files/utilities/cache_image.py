from urllib.parse import urljoin
from files import models as fimods
from files.utilities.get_mime_type import get_mime_type
from everybase import settings
import boto3

def cache_image(image):
    """Save image as cache, record file, return file ID and cache URL
    
    Parameters:
    image
        Image object from Django form's cleaned_data. E.g.,
        form.cleaned_data['img']
    """
    mime_type = get_mime_type(image)
    file = fimods.File.objects.create(
        mime_type=mime_type,
        filename=image.name,
        s3_bucket_name=settings.AWS_STORAGE_BUCKET_NAME
    )

    key = settings.AWS_S3_KEY_CACHE_IMAGE % file.id

    file.s3_object_key = key
    file.save()

    s3 = boto3.session.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    ).resource('s3')

    # Save image
    s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
        Key=key,
        Body=image,
        ContentType=mime_type
    )

    return file.id, urljoin(settings.MEDIA_URL, key)