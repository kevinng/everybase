from django.template.response import TemplateResponse

def inbox(request):
    template_name = 'documents/inbox.html'
    return TemplateResponse(request, template_name, {'location': 'inbox'})

def documents(request):
    template_name = 'documents/inbox.html'
    return TemplateResponse(request, template_name, {'location': 'documents'})

def sent(request):
    template_name = 'documents/inbox.html'
    return TemplateResponse(request, template_name, {'location': 'sent'})

def materials(request):
    template_name = 'documents/inbox.html'
    return TemplateResponse(request, template_name, {'location': 'materials'})

def colleagues(request):
    template_name = 'documents/inbox.html'
    return TemplateResponse(request, template_name, {'location': 'colleagues'})

def r(request, file_to_render):
    template_name = 'documents/%s' % file_to_render
    return TemplateResponse(request, template_name, {})