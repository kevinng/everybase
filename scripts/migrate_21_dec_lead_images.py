import boto3
from everybase import settings
from files import models as fimods
from PIL import Image, ImageOps
from io import BytesIO

# Migrate files in production from pre 19 Apr 22
def run():
    print('Initializing boto3 S3 session')
    s3 = boto3.session.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    ).resource('s3')

    fs = fimods.File.objects.all()
    for f in fs:
        print('Processing file ' + str(f.id))

        if f.lead is None:
            # Skip this file, it's not associated with any lead
            print('Skipping file ' + str(f.id))
            continue

        f.presigned_url_issued = None
        f.presigned_url_lifespan = None
        f.presigned_url_response = None
        f.s3_bucket_name = settings.AWS_STORAGE_BUCKET_NAME

        key = settings.AWS_S3_KEY_LEAD_IMAGE % (f.lead.id, f.id)

        # Copy from current location
        lead_s3_obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, key)\
            .copy_from(CopySource={
                'Bucket': 'ebproduction', # Current bucket, access should be given temporarily
                'Key': f.s3_object_key # Current key
            })

        thumb_key = settings.AWS_S3_KEY_LEAD_IMAGE_THUMBNAIL % (f.lead.id, f.id)

        f.s3_object_key = key # Update key
        f.thumbnail_s3_object_key = thumb_key
        f.e_tag = lead_s3_obj.get('ETag')
        f.last_modified = lead_s3_obj.get('LastModified')
        f.save()

        # Download image for resize to thumbnail
        cache = BytesIO()
        s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)\
            .download_fileobj(key, cache)
        cache.seek(0)

        # Resize and save thumbnail, and record sizes
        with Image.open(cache) as im:
            # Resize preserving aspect ratio cropping from the center
            thumbnail = ImageOps.fit(im, settings.LEAD_IMAGE_THUMBNAIL_SIZE)
            output = BytesIO()
            thumbnail.save(output, format='PNG')
            output.seek(0)

            s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
                Key=thumb_key,
                Body=output,
                ContentType=f.mime_type
            )

            f.width, f.height = im.size
            f.thumbnail_width, f.thumbnail_height = thumbnail.size
            f.save()