from . import models
from . import serializers
from rest_framework import generics, permissions

class IncotermAPI():
    queryset = models.Incoterm.objects.all()
    serializer_class = serializers.IncotermSerializer
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
    queryset = models.Currency.objects.all()
    serializer_class = serializers.CurrencySerializer
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
    queryset = models.PaymentMode.objects.all()
    serializer_class = serializers.PaymentModeSerializer
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
    queryset = models.ContactType.objects.all()
    serializer_class = serializers.ContactTypeSerializer
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
    queryset = models.LeadCategory.objects.all()
    serializer_class = serializers.LeadCategorySerializer
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
    queryset = models.MatchMethod.objects.all()
    serializer_class = serializers.MatchMethodSerializer
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
    queryset = models.MatchStatus.objects.all()
    serializer_class = serializers.MatchStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

class MatchStatusList(MatchStatusAPI, generics.ListCreateAPIView):
    pass

class MatchStatusDetail(MatchStatusAPI, generics.RetrieveUpdateDestroyAPIView):
    pass

class SupplyQuoteAPI():
    queryset = models.SupplyQuoteStatus.objects.all()
    serializer_class = serializers.SupplyQuoteStatusSerializer
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
    queryset = models.DemandQuoteStatus.objects.all()
    serializer_class = serializers.DemandQuoteStatusSerializer
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
    queryset = models.UnitOfMeasure.objects.all()
    serializer_class = serializers.UnitOfMeasureSerializer
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
    queryset = models.UOMRelationship.objects.all()
    serializer_class = serializers.UOMRelationshipSerializer
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
    queryset = models.Supply.objects.all()
    serializer_class = serializers.SupplySerializer
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
    queryset = models.Demand.objects.all()
    serializer_class = serializers.DemandSerializer
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
    queryset = models.SupplyQuote.objects.all()
    serializer_class = serializers.SupplyQuoteSerializer
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
    queryset = models.ProductionCapability.objects.all()
    serializer_class = serializers.ProductionCapabilitySerializer
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
    queryset = models.DemandQuote.objects.all()
    serializer_class = serializers.DemandQuoteSerializer
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
    queryset = models.Trench.objects.all()
    serializer_class = serializers.TrenchSerializer
    permission_classes = [permissions.IsAuthenticated]

class TrenchList(
    TrenchAPI,
    generics.ListCreateAPIView):
    pass

class TrenchDetail(
    TrenchAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class MatchAPI():
    queryset = models.Match.objects.all()
    serializer_class = serializers.MatchSerializer
    permission_classes = [permissions.IsAuthenticated]

class MatchList(
    MatchAPI,
    generics.ListCreateAPIView):
    pass

class MatchDetail(
    MatchAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class SupplyCommissionAPI():
    queryset = models.SupplyCommission.objects.all()
    serializer_class = serializers.SupplyCommissionSerializer
    permission_classes = [permissions.IsAuthenticated]

class SupplyCommissionList(
    SupplyCommissionAPI,
    generics.ListCreateAPIView):
    pass

class SupplyCommissionDetail(
    SupplyCommissionAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class DemandCommissionAPI():
    queryset = models.DemandCommission.objects.all()
    serializer_class = serializers.DemandCommissionSerializer
    permission_classes = [permissions.IsAuthenticated]

class DemandCommissionList(
    DemandCommissionAPI,
    generics.ListCreateAPIView):
    pass

class DemandCommissionDetail(
    DemandCommissionAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass