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

class GmassCampaignResultList(generics.ListCreateAPIView):
    queryset = GmassCampaignResult.objects.all()
    serializer_class = GmassCampaignResultSerializer
    permission_classes = [permissions.IsAuthenticated]

class GmassCampaignResultDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GmassCampaignResult.objects.all()
    serializer_class = GmassCampaignResultSerializer
    permission_classes = [permissions.IsAuthenticated]

class GmassCampaignList(generics.ListCreateAPIView):
    queryset = GmassCampaign.objects.all()
    serializer_class = GmassCampaignSerializer
    permission_classes = [permissions.IsAuthenticated]

class GmassCampaignDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GmassCampaign.objects.all()
    serializer_class = GmassCampaignSerializer
    permission_classes = [permissions.IsAuthenticated]

class ChemicalClusterOfSingaporeResultList(generics.ListCreateAPIView):
    queryset = ChemicalClusterOfSingaporeResult.objects.all()
    serializer_class = ChemicalClusterOfSingaporeResultSerializer
    permission_classes = [permissions.IsAuthenticated]

class ChemicalClusterOfSingaporeResultDetail(
        generics.RetrieveUpdateDestroyAPIView):
    queryset = ChemicalClusterOfSingaporeResult.objects.all()
    serializer_class = ChemicalClusterOfSingaporeResultSerializer
    permission_classes = [permissions.IsAuthenticated]

class Fibre2FashionResultList(generics.ListCreateAPIView):
    queryset = Fibre2FashionResult.objects.all()
    serializer_class = Fibre2FashionResultSerializer
    permission_classes = [permissions.IsAuthenticated]

class Fibre2FashionResultDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Fibre2FashionResult.objects.all()
    serializer_class = Fibre2FashionResultSerializer
    permission_classes = [permissions.IsAuthenticated]

class ZeroBounceResultList(generics.ListCreateAPIView):
    queryset = ZeroBounceResult.objects.all()
    serializer_class = ZeroBounceResultSerializer
    permission_classes = [permissions.IsAuthenticated]

class ZeroBounceResultDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ZeroBounceResult.objects.all()
    serializer_class = ZeroBounceResultSerializer
    permission_classes = [permissions.IsAuthenticated]

class DataSourceList(generics.ListCreateAPIView):
    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializer
    permission_classes = [permissions.IsAuthenticated]

class DataSourceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializer
    permission_classes = [permissions.IsAuthenticated]

class SourcedEmailList(generics.ListCreateAPIView):
    queryset = SourcedEmail.objects.all()
    serializer_class = SourcedEmailSerializer
    permission_classes = [permissions.IsAuthenticated]

class SourcedEmailDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SourcedEmail.objects.all()
    serializer_class = SourcedEmailSerializer
    permission_classes = [permissions.IsAuthenticated]

class ChemicalBookResultList(generics.ListCreateAPIView):
    queryset = ChemicalBookResult.objects.all()
    serializer_class = ChemicalBookResultSerializer
    permission_classes = [permissions.IsAuthenticated]

class ChemicalBookResultDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ChemicalBookResult.objects.all()
    serializer_class = ChemicalBookResultSerializer
    permission_classes = [permissions.IsAuthenticated]

class LookChemResultList(generics.ListCreateAPIView):
    queryset = LookChemResult.objects.all()
    serializer_class = LookChemResultSerializer
    permission_classes = [permissions.IsAuthenticated]

class LookChemResultDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = LookChemResult.objects.all()
    serializer_class = LookChemResultSerializer
    permission_classes = [permissions.IsAuthenticated]

class WorldOfChemicalResultList(generics.ListCreateAPIView):
    queryset = WorldOfChemicalsResult.objects.all()
    serializer_class = WorldOfChemicalResultSerializer
    permission_classes = [permissions.IsAuthenticated]

class WorldOfChemicalResultDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorldOfChemicalsResult.objects.all()
    serializer_class = WorldOfChemicalResultSerializer
    permission_classes = [permissions.IsAuthenticated]