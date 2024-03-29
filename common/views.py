from django.http import HttpResponse
from django.template.response import TemplateResponse
# from django.http import HttpResponse, HttpResponseRedirect
# from django.urls import reverse

# from leads import models as lemods

def ads_txt(_):
    filename = 'ads.txt'
    content = 'google.com, pub-4994829786974999, DIRECT, f08c47fec0942fa0'
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response

def privacy(request):
    template_name = 'privacy.html'
    return TemplateResponse(request, template_name, {})

def terms(request):
    template_name = 'terms.html'
    return TemplateResponse(request, template_name, {})







def pricing(request):
    template_name = 'pricing.html'
    return TemplateResponse(request, template_name, {})

def earn_money(request):
    template_name = 'earn_money.html'
    return TemplateResponse(request, template_name, {})

def faq(request):
    template_name = 'faq.html'
    return TemplateResponse(request, template_name, {})

def home(request):
    template_name = 'home.html'
    return TemplateResponse(request, template_name, {})

# def e(request, file_to_render):
#     template_name = 'examples/%s' % file_to_render
#     return TemplateResponse(request, template_name, {})

# def m(request, file_to_render):
#     template_name = 'mock_ups/%s' % file_to_render
#     return TemplateResponse(request, template_name, {})

# def sm(request, file_to_render):
#     template_name = 'superio/mock_ups/%s' % file_to_render
#     return TemplateResponse(request, template_name, {})

# def ml(request, file_to_render):
#     template_name = 'metronic/layout_builder/%s' % file_to_render
#     return TemplateResponse(request, template_name, {})

# def mm(request, file_to_render):
#     template_name = 'metronic/mock_ups/%s' % file_to_render
#     return TemplateResponse(request, template_name, {})



# def home(request):
#     # Redirect to dashboard if user is authenticated
#     if request.user.is_authenticated:
#         return HttpResponseRedirect(reverse('leads:lead_create'))

#     leads = lemods.Lead.objects.filter(
#         deleted__isnull=True
#     ).order_by('-created')[0:6]

#     return TemplateResponse(request, 'superio/home.html', {'leads': leads})







# from . import models
# from . import serializers
# from django.http import JsonResponse
# from rest_framework.parsers import JSONParser
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework import generics, permissions

# class CountryAPI():
#     queryset = models.Country.objects.all()
#     serializer_class = serializers.CountrySerializer
#     permission_classes = [permissions.IsAuthenticated]

# class CountryList(
#     CountryAPI,
#     generics.ListCreateAPIView):
#     pass

# class CountryDetail(
#     CountryAPI,
#     generics.RetrieveUpdateDestroyAPIView):
#     pass

# class StateAPI():
#     queryset = models.State.objects.all()
#     serializer_class = serializers.StateSerializer
#     permission_classes = [permissions.IsAuthenticated]

# class StateList(
#     StateAPI,
#     generics.ListCreateAPIView):
#     pass

# class StateDetail(
#     StateAPI,
#     generics.RetrieveUpdateDestroyAPIView):
#     pass

# class ImportJobAPI():
#     queryset = models.ImportJob.objects.all()
#     serializer_class = serializers.ImportJobSerializer
#     permission_classes = [permissions.IsAuthenticated]

# class ImportJobList(
#     ImportJobAPI,
#     generics.ListCreateAPIView):
#     pass

# class ImportJobDetail(
#     ImportJobAPI,
#     generics.RetrieveUpdateDestroyAPIView):
#     pass

# def pricing(request):
#     return TemplateResponse(request, 'pricing.html', {})

# def home(request):
#     return TemplateResponse(request, 'home.html', {})