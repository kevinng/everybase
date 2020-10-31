from .models import (Incoterm, Currency, PaymentMode, ContactType, LeadCategory,
    MatchMethod, MatchStatus, SupplyQuoteStatus, DemandQuoteStatus)
from .serializers import (IncotermSerializer, CurrencySerializer,
    PaymentModeSerializer, ContactTypeSerializer, LeadCategorySerializer,
    MatchMethodSerializer, MatchStatusSerializer, SupplyQuoteStatusSerializer,
    DemandQuoteStatusSerializer)
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

class LeadCategoryList(generics.ListCreateAPIView):
    queryset = LeadCategory.objects.all()
    serializer_class = LeadCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class LeadCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = LeadCategory.objects.all()
    serializer_class = LeadCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class MatchMethodList(generics.ListCreateAPIView):
    queryset = MatchMethod.objects.all()
    serializer_class = MatchMethodSerializer
    permission_classes = [permissions.IsAuthenticated]

class MatchMethodDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MatchMethod.objects.all()
    serializer_class = MatchMethodSerializer
    permission_classes = [permissions.IsAuthenticated]

class MatchStatusList(generics.ListCreateAPIView):
    queryset = MatchStatus.objects.all()
    serializer_class = MatchStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

class MatchStatusDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MatchStatus.objects.all()
    serializer_class = MatchStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

class SupplyQuoteStatusList(generics.ListCreateAPIView):
    queryset = SupplyQuoteStatus.objects.all()
    serializer_class = SupplyQuoteStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

class SupplyQuoteStatusDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SupplyQuoteStatus.objects.all()
    serializer_class = SupplyQuoteStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

class DemandQuoteStatusList(generics.ListCreateAPIView):
    queryset = DemandQuoteStatus.objects.all()
    serializer_class = DemandQuoteStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

class DemandQuoteStatusDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DemandQuoteStatus.objects.all()
    serializer_class = DemandQuoteStatusSerializer
    permission_classes = [permissions.IsAuthenticated]