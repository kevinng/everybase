from . import serializers, models
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