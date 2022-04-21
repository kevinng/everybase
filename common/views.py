from . import models
from . import serializers
# from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.http import HttpResponse
# from rest_framework.parsers import JSONParser
# from django.views.decorators.csrf import csrf_exempt
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

def e(request, file_to_render):
    template_name = 'examples/%s' % file_to_render
    return TemplateResponse(request, template_name, {})

def m(request, file_to_render):
    template_name = 'mock_ups/%s' % file_to_render
    return TemplateResponse(request, template_name, {})

def home(request):
    return TemplateResponse(request, 'home.html', {})

def pricing(request):
    return TemplateResponse(request, 'pricing.html', {})

def ads_txt(request):
    filename = "ads.txt"
    content = 'google.com, pub-4994829786974999, DIRECT, f08c47fec0942fa0'
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response