from .models import (Incoterm, Currency, PaymentMode, ContactType, LeadCategory,
    MatchMethod, MatchStatus, SupplyQuoteStatus, DemandQuoteStatus,
    UnitOfMeasure, UOMRelationship, Supply, Demand)
from .serializers import (IncotermSerializer, CurrencySerializer,
    PaymentModeSerializer, ContactTypeSerializer, LeadCategorySerializer,
    MatchMethodSerializer, MatchStatusSerializer, SupplyQuoteStatusSerializer,
    DemandQuoteStatusSerializer, UnitOfMeasureSerializer,
    UOMRelationshipSerializer, SupplySerializer, DemandSerializer)
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

class UnitOfMeasureList(generics.ListCreateAPIView):
    queryset = UnitOfMeasure.objects.all()
    serializer_class = UnitOfMeasureSerializer
    permission_classes = [permissions.IsAuthenticated]

class UnitOfMeasureDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UnitOfMeasure.objects.all()
    serializer_class = UnitOfMeasureSerializer
    permission_classes = [permissions.IsAuthenticated]

class UOMRelationshipList(generics.ListCreateAPIView):
    queryset = UOMRelationship.objects.all()
    serializer_class = UOMRelationshipSerializer
    permission_classes = [permissions.IsAuthenticated]

class UOMRelationshipDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UOMRelationship.objects.all()
    serializer_class = UOMRelationshipSerializer
    permission_classes = [permissions.IsAuthenticated]

class SupplyList(generics.ListCreateAPIView):
    queryset = Supply.objects.all()
    serializer_class = SupplySerializer
    permission_classes = [permissions.IsAuthenticated]

class SupplyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Supply.objects.all()
    serializer_class = SupplySerializer
    permission_classes = [permissions.IsAuthenticated]

class DemandList(generics.ListCreateAPIView):
    queryset = Demand.objects.all()
    serializer_class = DemandSerializer
    permission_classes = [permissions.IsAuthenticated]

class DemandDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Demand.objects.all()
    serializer_class = DemandSerializer
    permission_classes = [permissions.IsAuthenticated]