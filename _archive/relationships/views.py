from . import models
# from . import serializers
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend

class PhoneNumberTypeAPI():
    queryset = models.PhoneNumberType.objects.all()
    serializer_class = serializers.PhoneNumberTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class PhoneNumberTypeList(
    PhoneNumberTypeAPI,
    generics.ListCreateAPIView):
    pass

class PhoneNumberTypeDetail(
    PhoneNumberTypeAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class PhoneNumberAPI():
    queryset = models.PhoneNumber.objects.all()
    serializer_class = serializers.PhoneNumberSerializer
    permission_classes = [permissions.IsAuthenticated]

class PhoneNumberList(
    PhoneNumberAPI,
    generics.ListCreateAPIView):
    pass

class PhoneNumberDetail(
    PhoneNumberAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class EmailAPI():
    queryset = models.Email.objects.all()
    serializer_class = serializers.EmailSerializer
    permission_classes = [permissions.IsAuthenticated]

class EmailList(
    EmailAPI,
    generics.ListCreateAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['email']

class EmailDetail(
    EmailAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class InvalidEmailAPI():
    queryset = models.InvalidEmail.objects.all()
    serializer_class = serializers.InvalidEmailSerializer
    permission_classes = [permissions.IsAuthenticated]

class InvalidEmailList(
    InvalidEmailAPI,
    generics.ListCreateAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['email']

class InvalidEmailDetail(
    InvalidEmailAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass