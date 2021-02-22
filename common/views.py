from . import models
from . import serializers
from django.http import JsonResponse
from django.template.response import TemplateResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
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

class ImportJobAPI():
    queryset = models.ImportJob.objects.all()
    serializer_class = serializers.ImportJobSerializer
    permission_classes = [permissions.IsAuthenticated]

class ImportJobList(
    ImportJobAPI,
    generics.ListCreateAPIView):
    pass

class ImportJobDetail(
    ImportJobAPI,
    generics.RetrieveUpdateDestroyAPIView):
    pass

@csrf_exempt
def post_dump(request):
    """
    Dump all HTTP call parameters into the console.
    """
    print(request)
    print(request.POST)
    print(request.META)
    print(request.body)
    # if request.method == 'POST':
    #     data = JSONParser().parse(request)
    #     print(data) # Output post data to log
    #     return JsonResponse(data, status=200)

    return JsonResponse({}, status=200)

def r(request, file_to_render):
    template_name = 'examples/%s' % file_to_render
    return TemplateResponse(request, template_name, {})