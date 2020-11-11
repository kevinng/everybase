from django.shortcuts import render, redirect
from .models import CloakedLink
from django.template.response import TemplateResponse

def direct(request, key):
    cloaked_link = CloakedLink.objects.get(pk=key)

    if cloaked_link.redirect == True:
        return redirect(cloaked_link.url)

    context = { 'cloaked_link': cloaked_link }
    return render(request, 'cloaker/iframe.html', context)

def r(request, file_to_render):
    template_name = 'cloaker/%s' % file_to_render
    return TemplateResponse(request, template_name, {})