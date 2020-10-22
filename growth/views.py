from .models import GmassCampaignResult
from .serializers import GmassCampaignResultSerializer
from rest_framework import generics

class GmassCampaignResultList(generics.ListCreateAPIView):
    queryset = GmassCampaignResult.objects.all()
    serializer_class = GmassCampaignResultSerializer

class GmassCampaignResultDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GmassCampaignResult.objects.all()
    serializer_class = GmassCampaignResultSerializer