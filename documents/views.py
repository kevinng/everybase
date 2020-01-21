from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.shortcuts import render
from django.views import generic

from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions

from .forms import DocumentForm
from .models import (
    Document, DocumentType, File, CreateFilePresignedURL)
from .serializers import CreateFilePresignedURLSerializer
from materials.models import Material
from accounts.models import Account

class CreateFilePresignedURLView(
    mixins.CreateModelMixin,
    generics.GenericAPIView):
    serializer_class = CreateFilePresignedURLSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        account = Account.objects.get(pk=self.request.user)
        serializer.save(requester=account)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class DocumentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Document
    form_class = DocumentForm
    template_name = 'documents/document_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Materials for active organization
        account = Account.objects.get(pk=self.request.user)
        materials = Material.objects.filter(
            organization=account.active_organization
        ).order_by('-name')
        context['materials'] = materials

        # Document types
        context['document_types'] = DocumentType.objects.all()

        return context

@login_required
def document_create(request):
    if request.method == 'POST':
        account = Account.objects.get(pk=request.user)
        if account.active_organization == None:
            # Document created must tie to active organization.
            return render(request, 'errors/access_denied.html')
        
        form = DocumentForm(request.POST)
        if form.is_valid():

            return HttpResponseRedirect(reverse('documents:list'))
    else:
        form = DocumentForm()

    return render(request, 'documents/document_create.html', {'form': form})

def documents(request):
    template_name = 'documents/document_list.html'
    return TemplateResponse(request, template_name, {'location': 'documents'})

def inbox(request):
    template_name = 'documents/inbox.html'
    return TemplateResponse(request, template_name, {'location': 'inbox'})

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