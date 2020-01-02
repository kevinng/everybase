from django.http import HttpResponse
from django.template import loader

def r(request, file_to_render):
    template = loader.get_template('documents/%s' % file_to_render)
    return HttpResponse(template.render({}, request))