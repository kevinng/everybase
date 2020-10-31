from .models import (Incoterm, Currency, PaymentMode, ContactType, LeadCategory,
    MatchMethod, MatchStatus, SupplyQuoteStatus, DemandQuoteStatus,
    UnitOfMeasure, UOMRelationship, Supply, Demand, SupplyQuote,
    ProductionCapability, DemandQuote, Trench)
from .serializers import (IncotermSerializer, CurrencySerializer,
    PaymentModeSerializer, ContactTypeSerializer, LeadCategorySerializer,
    MatchMethodSerializer, MatchStatusSerializer, SupplyQuoteStatusSerializer,
    DemandQuoteStatusSerializer, UnitOfMeasureSerializer,
    UOMRelationshipSerializer, SupplySerializer, DemandSerializer,
    SupplyQuoteSerializer, ProductionCapabilitySerializer,
    DemandQuoteSerializer, TrenchSerializer)
from rest_framework import generics, permissions

class IncotermAPI():
    queryset = Incoterm.objects.all()
    serializer_class = IncotermSerializer
    permission_classes = [permissions.IsAuthenticated]

class IncotermList(
    IncotermAPI,
    generics.ListCreateAPIView):
    pass

class IncotermDetail(
    IncotermAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class CurrencyAPI():
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [permissions.IsAuthenticated]

class CurrencyList(
    CurrencyAPI,
    generics.ListCreateAPIView):
    pass

class CurrencyDetail(
    CurrencyAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class PaymentModeAPI():
    queryset = PaymentMode.objects.all()
    serializer_class = PaymentModeSerializer
    permission_classes = [permissions.IsAuthenticated]

class PaymentModeList(
    PaymentModeAPI,
    generics.ListCreateAPIView):
    pass

class PaymentModeDetail(
    PaymentModeAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class ContactTypeAPI():
    queryset = ContactType.objects.all()
    serializer_class = ContactTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class ContactTypeList(
    ContactTypeAPI,
    generics.ListCreateAPIView):
    pass

class ContactTypeDetail(
    ContactTypeAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class LeadCategoryAPI():
    queryset = LeadCategory.objects.all()
    serializer_class = LeadCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class LeadCategoryList(
    LeadCategoryAPI,
    generics.ListCreateAPIView):
    pass

class LeadCategoryDetail(
    LeadCategoryAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class MatchMethodAPI():
    queryset = MatchMethod.objects.all()
    serializer_class = MatchMethodSerializer
    permission_classes = [permissions.IsAuthenticated]

class MatchMethodList(
    MatchMethodAPI,
    generics.ListCreateAPIView):
    pass

class MatchMethodDetail(
    MatchMethodAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class MatchStatusAPI():
    queryset = MatchStatus.objects.all()
    serializer_class = MatchStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

class MatchStatusList(MatchStatusAPI, generics.ListCreateAPIView):
    pass

class MatchStatusDetail(MatchStatusAPI, generics.RetrieveUpdateDestroyAPIView):
    pass

class SupplyQuoteAPI():
    queryset = SupplyQuoteStatus.objects.all()
    serializer_class = SupplyQuoteStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

class SupplyQuoteStatusList(
    SupplyQuoteAPI,
    generics.ListCreateAPIView):
    pass

class SupplyQuoteStatusDetail(
    SupplyQuoteAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class DemandQuoteStatusAPI():
    queryset = DemandQuoteStatus.objects.all()
    serializer_class = DemandQuoteStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

class DemandQuoteStatusList(
    DemandQuoteStatusAPI,
    generics.ListCreateAPIView):
    pass

class DemandQuoteStatusDetail(
    DemandQuoteStatusAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class UnitOfMeasureAPI():
    queryset = UnitOfMeasure.objects.all()
    serializer_class = UnitOfMeasureSerializer
    permission_classes = [permissions.IsAuthenticated]

class UnitOfMeasureList(
    UnitOfMeasureAPI,
    generics.ListCreateAPIView):
    pass

class UnitOfMeasureDetail(
    UnitOfMeasureAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class UOMRelationshipAPI():
    queryset = UOMRelationship.objects.all()
    serializer_class = UOMRelationshipSerializer
    permission_classes = [permissions.IsAuthenticated]

class UOMRelationshipList(
    UOMRelationshipAPI,
    generics.ListCreateAPIView):
    pass

class UOMRelationshipDetail(
    UOMRelationshipAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class SupplyAPI():
    queryset = Supply.objects.all()
    serializer_class = SupplySerializer
    permission_classes = [permissions.IsAuthenticated]

class SupplyList(
    SupplyAPI,
    generics.ListCreateAPIView):
    pass

class SupplyDetail(
    SupplyAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class DemandAPI():
    queryset = Demand.objects.all()
    serializer_class = DemandSerializer
    permission_classes = [permissions.IsAuthenticated]

class DemandList(
    DemandAPI,
    generics.ListCreateAPIView):
    pass

class DemandDetail(
    DemandAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class SupplyQuoteAPI():
    queryset = SupplyQuote.objects.all()
    serializer_class = SupplyQuoteSerializer
    permission_classes = [permissions.IsAuthenticated]

class SupplyQuoteList(
    SupplyQuoteAPI,
    generics.ListCreateAPIView):
    pass

class SupplyQuoteDetail(
    SupplyQuoteAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class ProductionCapabilityAPI():
    queryset = ProductionCapability.objects.all()
    serializer_class = ProductionCapabilitySerializer
    permission_classes = [permissions.IsAuthenticated]

class ProductionCapabilityList(
    ProductionCapabilityAPI,
    generics.ListCreateAPIView):
    pass

class ProductionCapabilityDetail(
    ProductionCapabilityAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class DemandQuoteAPI():
    queryset = DemandQuote.objects.all()
    serializer_class = DemandQuoteSerializer
    permission_classes = [permissions.IsAuthenticated]

class DemandQuoteList(
    DemandQuoteAPI,
    generics.ListCreateAPIView):
    pass

class DemandQuoteDetail(
    DemandQuoteAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class TrenchAPI():
    queryset = Trench.objects.all()
    serializer_class = TrenchSerializer
    permission_classes = [permissions.IsAuthenticated]

class TrenchList(
    TrenchAPI,
    generics.ListCreateAPIView):
    pass

class TrenchDetail(
    TrenchAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass