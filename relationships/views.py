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

class PersonLinkAPI():
    queryset = models.PersonLink.objects.all()
    serializer_class = serializers.PersonLinkSerializer
    permission_classes = [permissions.IsAuthenticated]

class PersonLinkList(
    PersonLinkAPI,
    generics.ListCreateAPIView):
    pass

class PersonLinkDetail(
    PersonLinkAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class PersonCompanyTypeAPI():
    queryset = models.PersonCompanyType.objects.all()
    serializer_class = serializers.PersonCompanyTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class PersonCompanyTypeList(
    PersonCompanyTypeAPI,
    generics.ListCreateAPIView):
    pass

class PersonCompanyTypeDetail(
    PersonCompanyTypeAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass