from . import serializers
from rest_framework import mixins, generics

class ReadFileView(
    mixins.CreateModelMixin,
    generics.GenericAPIView):
    """
    View to get AWS S3 object read-only pre-signed URLs for the specified file
    via a HTTP POST request.
    """
    serializer_class = serializers.ReadFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)