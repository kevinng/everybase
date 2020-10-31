from .models import (Incoterm, Currency, PaymentMode, ContactType)
from .serializers import (IncotermSerializer, CurrencySerializer,
    PaymentModeSerializer, ContactTypeSerializer)
from rest_framework import generics, permissions

class IncotermList(generics.ListCreateAPIView):
    queryset = Incoterm.objects.all()
    serializer_class = IncotermSerializer
    permission_classes = [permissions.IsAuthenticated]

class IncotermDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Incoterm.objects.all()
    serializer_class = IncotermSerializer
    permission_classes = [permissions.IsAuthenticated]

class CurrencyList(generics.ListCreateAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [permissions.IsAuthenticated]

class CurrencyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [permissions.IsAuthenticated]

class PaymentModeList(generics.ListCreateAPIView):
    queryset = PaymentMode.objects.all()
    serializer_class = PaymentModeSerializer
    permission_classes = [permissions.IsAuthenticated]

class PaymentModeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PaymentMode.objects.all()
    serializer_class = PaymentModeSerializer
    permission_classes = [permissions.IsAuthenticated]

class ContactTypeList(generics.ListCreateAPIView):
    queryset = ContactType.objects.all()
    serializer_class = ContactTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class ContactTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ContactType.objects.all()
    serializer_class = ContactTypeSerializer
    permission_classes = [permissions.IsAuthenticated]