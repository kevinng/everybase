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

class PersonCompanyAPI():
    queryset = models.PersonCompany.objects.all()
    serializer_class = serializers.PersonCompanySerializer
    permission_classes = [permissions.IsAuthenticated]

class PersonCompanyList(
    PersonCompanyAPI,
    generics.ListCreateAPIView):
    pass

class PersonCompanyDetail(
    PersonCompanyAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class PersonAddressTypeAPI():
    queryset = models.PersonAddressType.objects.all()
    serializer_class = serializers.PersonAddressTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class PersonAddressTypeList(
    PersonAddressTypeAPI,
    generics.ListCreateAPIView):
    pass

class PersonAddressTypeDetail(
    PersonAddressTypeAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class PersonAddressAPI():
    queryset = models.PersonAddress.objects.all()
    serializer_class = serializers.PersonAddressSerializer
    permission_classes = [permissions.IsAuthenticated]

class PersonAddressList(
    PersonAddressAPI,
    generics.ListCreateAPIView):
    pass

class PersonAddressDetail(
    PersonAddressAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class PersonPhoneNumberTypeAPI():
    queryset = models.PersonPhoneNumberType.objects.all()
    serializer_class = serializers.PersonPhoneNumberTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class PersonPhoneNumberTypeList(
    PersonPhoneNumberTypeAPI,
    generics.ListCreateAPIView):
    pass

class PersonPhoneNumberTypeDetail(
    PersonPhoneNumberTypeAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass