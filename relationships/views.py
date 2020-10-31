from . import models
from . import serializers
from rest_framework import generics, permissions

class PersonLinkTypeAPI():
    queryset = models.PersonLinkType.objects.all()
    serializer_class = serializers.PersonLinkTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class PersonLinkTypeList(
    PersonLinkTypeAPI,
    generics.ListCreateAPIView):
    pass

class PersonLinkTypeDetail(
    PersonLinkTypeAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass