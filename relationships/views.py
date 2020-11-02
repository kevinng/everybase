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

class PersonPhoneNumberAPI():
    queryset = models.PersonPhoneNumber.objects.all()
    serializer_class = serializers.PersonPhoneNumberSerializer
    permission_classes = [permissions.IsAuthenticated]

class PersonPhoneNumberList(
    PersonPhoneNumberAPI,
    generics.ListCreateAPIView):
    pass

class PersonPhoneNumberDetail(
    PersonPhoneNumberAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class PersonEmailTypeAPI():
    queryset = models.PersonEmailType.objects.all()
    serializer_class = serializers.PersonEmailTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class PersonEmailTypeList(
    PersonEmailTypeAPI,
    generics.ListCreateAPIView):
    pass

class PersonEmailTypeDetail(
    PersonEmailTypeAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class PersonEmailAPI():
    queryset = models.PersonEmail.objects.all()
    serializer_class = serializers.PersonEmailSerializer
    permission_classes = [permissions.IsAuthenticated]

class PersonEmailList(
    PersonEmailAPI,
    generics.ListCreateAPIView):
    pass

class PersonEmailDetail(
    PersonEmailAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class CompanyLinkTypeAPI():
    queryset = models.CompanyLinkType.objects.all()
    serializer_class = serializers.CompanyLinkTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class CompanyLinkTypeList(
    CompanyLinkTypeAPI,
    generics.ListCreateAPIView):
    pass

class CompanyLinkTypeDetail(
    CompanyLinkTypeAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class CompanyAddressTypeAPI():
    queryset = models.CompanyAddressType.objects.all()
    serializer_class = serializers.CompanyAddressTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class CompanyAddressTypeList(
    CompanyAddressTypeAPI,
    generics.ListCreateAPIView):
    pass

class CompanyAddressTypeDetail(
    CompanyAddressTypeAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class CompanyAddressAPI():
    queryset = models.CompanyAddress.objects.all()
    serializer_class = serializers.CompanyAddressSerializer
    permission_classes = [permissions.IsAuthenticated]

class CompanyAddressList(
    CompanyAddressAPI,
    generics.ListCreateAPIView):
    pass

class CompanyAddressDetail(
    CompanyAddressAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass