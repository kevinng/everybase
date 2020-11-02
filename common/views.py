from . import models
from . import serializers
from rest_framework import generics, permissions

class CountryAPI():
    queryset = models.Country.objects.all()
    serializer_class = serializers.CountrySerializer
    permission_classes = [permissions.IsAuthenticated]

class CountryList(
    CountryAPI,
    generics.ListCreateAPIView):
    pass

class CountryDetail(
    CountryAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass
