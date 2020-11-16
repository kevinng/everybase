from . import models
from . import serializers
from rest_framework import generics, permissions

class GmassCampaignResultAPI():
    queryset = models.GmassCampaignResult.objects.all()
    serializer_class = serializers.GmassCampaignResultSerializer
    permission_classes = [permissions.IsAuthenticated]

class GmassCampaignResultList(
    GmassCampaignResultAPI,
    generics.ListCreateAPIView):
    pass

class GmassCampaignResultDetail(
    GmassCampaignResultAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class GmassCampaignAPI():
    queryset = models.GmassCampaign.objects.all()
    serializer_class = serializers.GmassCampaignSerializer
    permission_classes = [permissions.IsAuthenticated]

class GmassCampaignList(
    GmassCampaignAPI,
    generics.ListCreateAPIView):
    pass

class GmassCampaignDetail(
    GmassCampaignAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class ChemicalClusterOfSingaporeCompanyAPI():
    queryset = models.ChemicalClusterOfSingaporeCompany.objects.all()
    serializer_class = serializers.ChemicalClusterOfSingaporeCompanySerializer
    permission_classes = [permissions.IsAuthenticated]

class ChemicalClusterOfSingaporeCompanyList(
    ChemicalClusterOfSingaporeCompanyAPI,
    generics.ListCreateAPIView):
    pass

class ChemicalClusterOfSingaporeCompanyDetail(
    ChemicalClusterOfSingaporeCompanyAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class ChemicalClusterOfSingaporeProductAPI():
    queryset = models.ChemicalClusterOfSingaporeProduct.objects.all()
    serializer_class = serializers.ChemicalClusterOfSingaporeProductSerializer
    permission_classes = [permissions.IsAuthenticated]

class ChemicalClusterOfSingaporeProductList(
    ChemicalClusterOfSingaporeProductAPI,
    generics.ListCreateAPIView):
    pass

class ChemicalClusterOfSingaporeProductDetail(
    ChemicalClusterOfSingaporeProductAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class ChemicalClusterOfSingaporeServiceAPI():
    queryset = models.ChemicalClusterOfSingaporeService.objects.all()
    serializer_class = serializers.ChemicalClusterOfSingaporeServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

class ChemicalClusterOfSingaporeServiceList(
    ChemicalClusterOfSingaporeServiceAPI,
    generics.ListCreateAPIView):
    pass

class ChemicalClusterOfSingaporeServiceDetail(
    ChemicalClusterOfSingaporeServiceAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class Fibre2FashionBuyingOfferAPI():
    queryset = models.Fibre2FashionBuyingOffer.objects.all()
    serializer_class = serializers.Fibre2FashionBuyingOfferSerializer
    permission_classes = [permissions.IsAuthenticated]

class Fibre2FashionBuyingOfferList(
    Fibre2FashionBuyingOfferAPI,
    generics.ListCreateAPIView):
    pass

class Fibre2FashionBuyingOfferDetail(
    Fibre2FashionBuyingOfferAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class Fibre2FashionSellingOfferAPI():
    queryset = models.Fibre2FashionSellingOffer.objects.all()
    serializer_class = serializers.Fibre2FashionSellingOfferSerializer
    permission_classes = [permissions.IsAuthenticated]

class Fibre2FashionSellingOfferList(
    Fibre2FashionSellingOfferAPI,
    generics.ListCreateAPIView):
    pass

class Fibre2FashionSellingOfferDetail(
    Fibre2FashionSellingOfferAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class ZeroBounceResultAPI():
    queryset = models.ZeroBounceResult.objects.all()
    serializer_class = serializers.ZeroBounceResultSerializer
    permission_classes = [permissions.IsAuthenticated]

class ZeroBounceResultList(
    ZeroBounceResultAPI,
    generics.ListCreateAPIView):
    pass

class ZeroBounceResultDetail(
    ZeroBounceResultAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class DataSourceAPI():
    queryset = models.DataSource.objects.all()
    serializer_class = serializers.DataSourceSerializer
    permission_classes = [permissions.IsAuthenticated]

class DataSourceList(
    DataSourceAPI,
    generics.ListCreateAPIView):
    pass

class DataSourceDetail(
    DataSourceAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class SourcedEmailAPI():
    queryset = models.SourcedEmail.objects.all()
    serializer_class = serializers.SourcedEmailSerializer
    permission_classes = [permissions.IsAuthenticated]

class SourcedEmailList(
    SourcedEmailAPI,
    generics.ListCreateAPIView):
    pass

class SourcedEmailDetail(
    SourcedEmailAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class ChemicalBookSupplierAPI():
    queryset = models.ChemicalBookSupplier.objects.all()
    serializer_class = serializers.ChemicalBookSupplierSerializer
    permission_classes = [permissions.IsAuthenticated]

class ChemicalBookSupplierList(
    ChemicalBookSupplierAPI,
    generics.ListCreateAPIView):
    pass

class ChemicalBookSupplierDetail(
    ChemicalBookSupplierAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class LookChemSupplierAPI():
    queryset = models.LookChemSupplier.objects.all()
    serializer_class = serializers.LookChemSupplierSerializer
    permission_classes = [permissions.IsAuthenticated]

class LookChemSupplierList(
    LookChemSupplierAPI,
    generics.ListCreateAPIView):
    pass

class LookChemSupplierDetail(
    LookChemSupplierAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class WorldOfChemicalsSupplierAPI():
    queryset = models.WorldOfChemicalsSupplier.objects.all()
    serializer_class = serializers.WorldOfChemicalSupplierSerializer
    permission_classes = [permissions.IsAuthenticated]

class WorldOfChemicalsSupplierList(
    WorldOfChemicalsSupplierAPI,
    generics.ListCreateAPIView):
    pass

class WorldOfChemicalsSupplierDetail(
    WorldOfChemicalsSupplierAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class OKChemBuyingRequestAPI():
    queryset = models.OKChemBuyingRequest.objects.all()
    serializer_class = serializers.OKChemBuyingRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

class OKChemBuyingRequestList(
    OKChemBuyingRequestAPI,
    generics.ListCreateAPIView):
    pass

class OKChemBuyingRequestDetail(
    OKChemBuyingRequestAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass