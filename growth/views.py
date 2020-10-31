from .models import (GmassCampaignResult, GmassCampaign,
    ChemicalClusterOfSingaporeResult, Fibre2FashionResult, ZeroBounceResult,
    DataSource, SourcedEmail, ChemicalBookResult, LookChemResult,
    WorldOfChemicalsResult)
from .serializers import (GmassCampaignResultSerializer,
    GmassCampaignSerializer, ChemicalClusterOfSingaporeResultSerializer,
    Fibre2FashionResultSerializer, ZeroBounceResultSerializer,
    DataSourceSerializer, SourcedEmailSerializer, ChemicalBookResultSerializer,
    LookChemResultSerializer, WorldOfChemicalResultSerializer)
from rest_framework import generics, permissions

class GmassCampaignResultAPI():
    queryset = GmassCampaignResult.objects.all()
    serializer_class = GmassCampaignResultSerializer
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
    queryset = GmassCampaign.objects.all()
    serializer_class = GmassCampaignSerializer
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
    queryset = ChemicalClusterOfSingaporeResult.objects.all()
    serializer_class = ChemicalClusterOfSingaporeResultSerializer
    permission_classes = [permissions.IsAuthenticated]

class ChemicalClusterOfSingaporeResultList(
    ChemicalClusterOfSingaporeResultAPI,
    generics.ListCreateAPIView):
    pass

class ChemicalClusterOfSingaporeResultDetail(
    ChemicalClusterOfSingaporeResultAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class Fibre2FashionResultAPI():
    queryset = Fibre2FashionResult.objects.all()
    serializer_class = Fibre2FashionResultSerializer
    permission_classes = [permissions.IsAuthenticated]

class Fibre2FashionResultList(
    Fibre2FashionResultAPI,
    generics.ListCreateAPIView):
    pass

class Fibre2FashionResultDetail(
    Fibre2FashionResultAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

class ZeroBounceResultAPI():
    queryset = ZeroBounceResult.objects.all()
    serializer_class = ZeroBounceResultSerializer
    permission_classes = [permissions.IsAuthenticated]

class ZeroBounceResultList(generics.ListCreateAPIView):
    pass

class ZeroBounceResultDetail(generics.RetrieveUpdateDestroyAPIView):
    pass

class DataSourceAPI():
    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializer
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
    queryset = SourcedEmail.objects.all()
    serializer_class = SourcedEmailSerializer
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
    queryset = ChemicalBookResult.objects.all()
    serializer_class = ChemicalBookResultSerializer
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
    queryset = LookChemResult.objects.all()
    serializer_class = LookChemResultSerializer
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
    queryset = WorldOfChemicalsResult.objects.all()
    serializer_class = WorldOfChemicalResultSerializer
    permission_classes = [permissions.IsAuthenticated]

class WorldOfChemicalResultList(
    WorldOfChemicalResultAPI,
    generics.ListCreateAPIView):
    pass

class WorldOfChemicalResultDetail(
    WorldOfChemicalResultAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass