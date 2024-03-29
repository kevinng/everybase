import boto3

from django.http import HttpResponse, Http404
from rest_framework import mixins, generics, permissions

from everybase import settings
from files import serializers, models
from relationships import models as relmods

class ReadOnlyPresignedURLView(
    mixins.CreateModelMixin,
    generics.GenericAPIView):
    """
    Get AWS S3 object read-only pre-signed URLs for the specified file via a
    HTTP POST request.
    """
    serializer_class = serializers.ReadOnlyPresignedURLSerializer
    permission_classes = [permissions.IsAuthenticated]
    # Note: provide a credentials for search engine to index those documents

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class WriteOnlyPresignedURLView(
    mixins.CreateModelMixin,
    generics.GenericAPIView):
    """
    Get AWS S3 object write-only pre-signed URLs for the specified file via a
    HTTP POST request.
    """
    serializer_class = serializers.WriteOnlyPresignedURLSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Note: associate the profile, not the Django user.
        uploader = relmods.User.objects.get(pk=self.request.user.user.id)
        serializer.save(uploader=uploader)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# TODO not in use
def get_file(_, uuid):
    """Redirect user to file in S3 with a pre-signed URL"""
    s3 = boto3.client('s3',
        region_name=settings.AWS_REGION_NAME,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    try:
        file = models.File.objects.get(uuid=uuid)
    except models.File.DoesNotExist:
        raise Http404('File does not exist')

    # Temporary redirect - prevents indexing of the S3 destination
    response = HttpResponse(status=302)
    url = s3.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
            'Key': file.s3_object_key
        },
        ExpiresIn=settings.AWS_PRESIGNED_URL_EXPIRES_IN
    )
    response['Location'] = url

    return response

##### Do not map these views to URLs #####

class FileList(generics.ListCreateAPIView):
    queryset = models.File.objects.all()
    serializer_class = serializers.FileSerializer

class FileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.File.objects.all()
    serializer_class = serializers.FileSerializer