import boto3
from botocore.exceptions import ClientError
from django.http import Http404
from rest_framework import serializers
from everybase import settings
from files.models import File
from datetime import datetime
import uuid

class ReadOnlyPresignedURLSerializer(serializers.Serializer):
    """
    Serializer class used to get AWS S3 object read-only pre-signed URLs for the
    specified file via a HTTP POST request.
    """

    file_id = serializers.IntegerField(write_only=True)
    issued = serializers.DateTimeField(read_only=True)
    lifespan = serializers.FloatField(read_only=True)
    url = serializers.URLField(read_only=True)

    def create(self, validated_data):
        """
        HTTP POST request to get a read-only pre-signed URL for reading the
        specified file on AWS S3.
        """
        try:
            file = File.objects.get(pk=validated_data['file_id'])
        except File.DoesNotExist:
            raise Http404

        s3 = boto3.client('s3',
            region_name=settings.AWS_REGION_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        issued = datetime.now()
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
    """
    Serializer class to get pre-signed URL to upload (i.e. write) the file via
    a HTTP POST request.
    """

    # Details of the pre-signed URL to upload (i.e. write) the file.
    file_id = serializers.IntegerField(read_only=True)
    issued = serializers.DateTimeField(read_only=True)
    lifespan = serializers.IntegerField(read_only=True)
    response = serializers.JSONField(read_only=True)

    def create(self, validated_data):
        """
        HTTP POST request to get a write-only pre-signed URL for uploading a
        file to AWS S3.
        """
        file = File(**validated_data)
        file.s3_bucket_name = settings.AWS_STORAGE_BUCKET_NAME

        timestamp = str(datetime.now()).split('.')[0]
        file.s3_object_key = f'{settings.AWS_S3_FILES_ROOT}/{timestamp}' + \
            f' - {str(uuid.uuid4())}'

        try:
            s3 = boto3.client('s3',
                region_name=settings.AWS_REGION_NAME,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )
            issued = datetime.now()
            response = s3.generate_presigned_post(
                Bucket=file.s3_bucket_name,
                Key=file.s3_object_key,
                Fields = {'acl': 'private'},
                Conditions = [{'acl': 'private'}],
                ExpiresIn=int(settings.AWS_PRESIGNED_URL_EXPIRES_IN)
            )

        except ClientError as e:
            logging.error(e)
            return None

        file.save()

        return {
            'file_id': file.id,
            'issued': issued,
            'lifespan': settings.AWS_PRESIGNED_URL_EXPIRES_IN,
            'response': response
        }
    
class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'upload_confirmed', 'uuid', 's3_bucket_name',
            's3_object_key', 's3_object_content_length', 's3_object_e_tag',
            's3_object_content_type', 's3_object_last_modified', 'details_md',
            'supplies', 'demands', 'issues', 'persons']