from django.template.response import TemplateResponse

def r(request, file_to_render):
    template_name = 'documents/%s' % file_to_render
    return TemplateResponse(request, template_name, {})