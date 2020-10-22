from .models import GmassCampaignResult, GmassCampaign
from .serializers import GmassCampaignResultSerializer, GmassCampaignSerializer
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