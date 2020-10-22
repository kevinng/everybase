from .models import GmassCampaignResult
from .serializers import GmassCampaignResultSerializer
from rest_framework import generics, permissions

class BulkListCreateAPIView(generics.ListCreateAPIView):
    def get_serializer(self, *args, **kwargs):
        """
        Override: if input 'data' is a list, set kwargs['many']=True, which
        returns a list serializer instead of a normal serializer.
        """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True

        return super(__class__, self).get_serializer(*args, **kwargs)

class GmassCampaignResultList(BulkListCreateAPIView):
    queryset = GmassCampaignResult.objects.all()
    serializer_class = GmassCampaignResultSerializer
    permission_classes = [permissions.IsAuthenticated]

class GmassCampaignResultDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GmassCampaignResult.objects.all()
    serializer_class = GmassCampaignResultSerializer
    permission_classes = [permissions.IsAuthenticated]