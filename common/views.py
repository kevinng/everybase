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

class StateAPI():
    queryset = models.State.objects.all()
    serializer_class = serializers.StateSerializer
    permission_classes = [permissions.IsAuthenticated]

class StateList(
    StateAPI,
    generics.ListCreateAPIView):
    pass

class StateDetail(
    StateAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass