import boto3
from botocore.exceptions import ClientError
import uuid, logging
from datetime import datetime
from rest_framework import serializers

from accounts.models import Account
from .models import File
from everybase.settings import (
    AWS_REGION_NAME, AWS_ACCESS_KEY_ID, AWS_STORAGE_BUCKET_NAME,
    AWS_SECRET_ACCESS_KEY, AWS_PRESIGNED_URL_EXPIRES_IN)

class ReadTempFileSerializer(serializers.Serializer):
    temp_file_id = serializers.UUIDField(write_only=True)
    issued = serializers.DateTimeField(read_only=True)
    lifespan = serializers.IntegerField(read_only=True)
    url = serializers.URLField(read_only=True)

    def create(self, validated_data):
        temp_file = File.objects.get(pk=validated_data['temp_file_id'])
        s3 = boto3.client('s3',
            region_name=AWS_REGION_NAME,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        issued = datetime.now() # Record time just before AWS call
        url = s3.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': AWS_STORAGE_BUCKET_NAME,
                'Key': temp_file.s3_object_key
            },
            ExpiresIn=AWS_PRESIGNED_URL_EXPIRES_IN
        )

        return {
            'issued': issued,
            'lifespan': AWS_PRESIGNED_URL_EXPIRES_IN,
            'url': url
        } 

class TempFileSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    presigned_url_issued = serializers.DateTimeField(read_only=True)
    presigned_url_lifespan = serializers.IntegerField(read_only=True)
    presigned_url_response = serializers.JSONField(read_only=True)
    filetype = serializers.CharField(write_only=True)

    def create(self, validated_data):
        temp_file = File(**validated_data)
        temp_file.presigned_url_lifespan = 3600
        temp_file.s3_bucket_name = AWS_STORAGE_BUCKET_NAME
        temp_file.s3_object_key = 'media/private/documents/%s/%s' % \
            (validated_data['creator'].id, temp_file.id)

        try:
            s3 = boto3.client('s3',
                region_name=AWS_REGION_NAME,
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY
            )
            response = s3.generate_presigned_post(
                Bucket=temp_file.s3_bucket_name,
                Key=temp_file.s3_object_key,
                Fields = {
                    'acl': 'private',
                    'Content-Type': temp_file.filetype
                },
                Conditions = [
                    {'acl': 'private'},
                    {'Content-Type': temp_file.filetype}
                ],
                ExpiresIn=temp_file.presigned_url_lifespan
            )

            temp_file.presigned_url_response = response
        except ClientError as e:
            logging.error(e)
            return None

        temp_file.save()
        return temp_file
    
    def update(self, instance, validated_data):
        # Only the filetype may be updated
        instance.filetype = validated_data.get('filetype', instance.filetype)
        instance.save()
        return instance