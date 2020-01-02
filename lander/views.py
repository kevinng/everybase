from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

# Create your views here.
def r(request, file_to_render):
    template = loader.get_template('lander/%s' % file_to_render)
    return HttpResponse(template.render({}, request))

def home(request):
    return render(request, 'lander/home.html')