from .models import (Incoterm, Currency)
from .serializers import (IncotermSerializer, CurrencySerializer)
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