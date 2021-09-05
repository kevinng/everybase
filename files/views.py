import boto3
from django.http import HttpResponse
from everybase.settings import (AWS_REGION_NAME, AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME,
    AWS_PRESIGNED_URL_EXPIRES_IN)
from files import serializers, models
from rest_framework import mixins, generics, permissions

class ReadOnlyPresignedURLView(
    mixins.CreateModelMixin,
    generics.GenericAPIView):
    # Note: following comment do not respect maximum line width so it shows up
    # properly (i.e. without linebreaks) in the browser.
    """
    Get AWS S3 object read-only pre-signed URLs for the specified file via a HTTP POST request.
    """
    serializer_class = serializers.ReadOnlyPresignedURLSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class WriteOnlyPresignedURLView(
    mixins.CreateModelMixin,
    generics.GenericAPIView):
    # Note: following comment do not respect maximum line width so it shows up
    # properly (i.e. without linebreaks) in the browser.
    """
    Get AWS S3 object write-only pre-signed URLs for the specified file via a HTTP POST request.
    """
    serializer_class = serializers.WriteOnlyPresignedURLSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class FileList(generics.ListCreateAPIView):
    queryset = models.File.objects.all()
    serializer_class = serializers.FileSerializer

class FileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.File.objects.all()
    serializer_class = serializers.FileSerializer

def get_file(_, id):
    """Redirect user to file in S3 with a pre-signed URL"""
    s3 = boto3.client('s3',
        region_name=AWS_REGION_NAME,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    file = models.File.objects.get(pk=id)

    response = HttpResponse(status=302) # Temporary redirect - prevents indexing
    response['Location'] = s3.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': AWS_STORAGE_BUCKET_NAME,
            'Key': file.s3_object_key
        },
        ExpiresIn=AWS_PRESIGNED_URL_EXPIRES_IN
    )

    return response