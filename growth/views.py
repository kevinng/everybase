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

class ChemicalClusterOfSingaporeResultAPI():
    queryset = models.ChemicalClusterOfSingaporeResult.objects.all()
    serializer_class = serializers.ChemicalClusterOfSingaporeResultSerializer
    permission_classes = [permissions.IsAuthenticated]

class ChemicalClusterOfSingaporeResultList(
    ChemicalClusterOfSingaporeResultAPI,
    generics.ListCreateAPIView):
    pass

class ChemicalClusterOfSingaporeResultDetail(
    ChemicalClusterOfSingaporeResultAPI,
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

class ChemicalBookResultAPI():
    queryset = models.ChemicalBookResult.objects.all()
    serializer_class = serializers.ChemicalBookResultSerializer
    permission_classes = [permissions.IsAuthenticated]

class ChemicalBookResultList(
    ChemicalBookResultAPI,
    generics.ListCreateAPIView):
    pass

class ChemicalBookResultDetail(
    ChemicalBookResultAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class LookChemResultAPI():
    queryset = models.LookChemResult.objects.all()
    serializer_class = serializers.LookChemResultSerializer
    permission_classes = [permissions.IsAuthenticated]

class LookChemResultList(
    LookChemResultAPI,
    generics.ListCreateAPIView):
    pass

class LookChemResultDetail(
    LookChemResultAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class WorldOfChemicalResultAPI():
    queryset = models.WorldOfChemicalsResult.objects.all()
    serializer_class = serializers.WorldOfChemicalResultSerializer
    permission_classes = [permissions.IsAuthenticated]

class WorldOfChemicalResultList(
    WorldOfChemicalResultAPI,
    generics.ListCreateAPIView):
    pass

class WorldOfChemicalResultDetail(
    WorldOfChemicalResultAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass