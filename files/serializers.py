import boto3, logging, pytz
from botocore.exceptions import ClientError
from datetime import datetime

from django.http import Http404
from rest_framework import serializers

from everybase import settings
from files import models as fimods

class ReadOnlyPresignedURLSerializer(serializers.Serializer):
    """Serializer class to get pre-signed URL to read file from S3.
    """
    uuid = serializers.UUIDField(read_only=True)
    presigned_url_issued = serializers.DateTimeField(read_only=True)
    presigned_url_lifespan = serializers.IntegerField(read_only=True)
    presigned_url_response = serializers.JSONField(read_only=True)
    file_type = serializers.CharField(read_only=True)

    def create(self, validated_data):
        """HTTP POST request to get a read-only pre-signed URL for reading the
        specified file on AWS S3.
        """
        try:
            file = fimods.File.objects.get(uuid=validated_data.get('uuid'))
        except fimods.File.DoesNotExist:
            raise Http404

        s3 = boto3.client('s3',
            region_name=settings.AWS_REGION_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        sgtz = pytz.timezone(settings.TIME_ZONE)
        issued = datetime.now(tz=sgtz)
        url = s3.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                'Key': file.s3_object_key
            },
            ExpiresIn=settings.AWS_PRESIGNED_URL_EXPIRES_IN
        )

        return {
            'issued': issued,
            'lifespan': settings.AWS_PRESIGNED_URL_EXPIRES_IN,
            'url': url
        }

class WriteOnlyPresignedURLSerializer(serializers.Serializer):
    """Serializer class to get pre-signed URL to upload (i.e. write) file to S3.
    """
    uuid = serializers.UUIDField(read_only=True)
    presigned_url_issued = serializers.DateTimeField(read_only=True)
    presigned_url_lifespan = serializers.IntegerField(read_only=True)
    presigned_url_response = serializers.JSONField(read_only=True)
    file_type = serializers.CharField(write_only=True)
    filename = serializers.CharField(write_only=True)

    def s3_object_key_prefix(self):
        return ''

    def create(self, validated_data):
        """
        HTTP POST request to get a write-only pre-signed URL for uploading a
        file to AWS S3.
        """
        file = fimods.File(**validated_data)
        file.presigned_url_lifespan = settings.AWS_PRESIGNED_URL_EXPIRES_IN
        file.s3_bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        file.s3_object_key = f'{self.s3_object_key_prefix()}{settings.AWS_S3_FILES_ROOT}/\
{str(datetime.now()).replace(" ", "_")}_{str(file.uuid)}'

        try:
            s3 = boto3.client('s3',
                region_name=settings.AWS_REGION_NAME,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )

            sgtz = pytz.timezone(settings.TIME_ZONE)
            file.presigned_url_issued = datetime.now(tz=sgtz)
            file.presigned_url_response = s3.generate_presigned_post(
                Bucket=file.s3_bucket_name,
                Key=file.s3_object_key,
                Fields = {
                    'acl': 'private',
                    'Content-Type': file.file_type
                },
                Conditions = [
                    {'acl': 'private'},
                    {'Content-Type': file.file_type}
                ],
                ExpiresIn=int(settings.AWS_PRESIGNED_URL_EXPIRES_IN)
            )

        except ClientError as e:
            logging.error(e)
            return None

        file.save()

        return {
            'uuid': file.uuid,
            'issued': file.presigned_url_issued,
            'lifespan': settings.AWS_PRESIGNED_URL_EXPIRES_IN,
            'response': file.presigned_url_response
        }

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = fimods.File
        fields = ['uuid', 'uploader', 'file_type', 'presigned_url_issued',
            'presigned_url_lifespan', 'presigned_url_response',
            's3_bucket_name', 's3_object_key', 's3_object_content_length',
            's3_object_e_tag', 's3_object_content_type',
            's3_object_last_modified']