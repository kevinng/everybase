from django.shortcuts import render
from .models import CloakedLink
from django.template.response import TemplateResponse

def iframe(request, key):
    context = {
        'cloaked_link': CloakedLink.objects.get(pk=key)
    }
    return render(request, 'cloaker/iframe.html', context)

def r(request, file_to_render):
    template_name = 'cloaker/%s' % file_to_render
    return TemplateResponse(request, template_name, {})