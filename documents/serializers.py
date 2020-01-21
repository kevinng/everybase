
from rest_framework import serializers
import boto3
from botocore.exceptions import ClientError
import uuid, datetime, logging

from accounts.models import Account
from .models import CreateFilePresignedURL
from everybase.settings import AWS_STORAGE_BUCKET_NAME

class CreateFilePresignedURLSerializer(serializers.Serializer):
    issued = serializers.DateTimeField(read_only=True)
    lifespan = serializers.IntegerField(read_only=True)
    response = serializers.JSONField(read_only=True)
    filetype = serializers.CharField(write_only=True)

    def create(self, validated_data):
        url = CreateFilePresignedURL(**validated_data)
        url.lifespan = 3600
        url.s3_bucket_name = AWS_STORAGE_BUCKET_NAME
        url.s3_object_key = 'media/private/documents/%s/%s' % \
            (validated_data['requester'].id, url.id)

        try:
            s3 = boto3.client('s3')
            response = s3.generate_presigned_post(
                Bucket=url.s3_bucket_name,
                Key=url.s3_object_key,
                ExpiresIn=url.lifespan
            )

            url.response = response
        except ClientError as e:
            logging.error(e)
            return None

        url.save()
        return url
    
    def update(self, instance, validated_data):
        # Only the filetype may be updated
        instance.filetype = validated_data.get('filetype', instance.filetype)
        instance.save()
        return instance