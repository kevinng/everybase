from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.urls import reverse

from rest_framework.authentication import SessionAuthentication
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from rest_framework import views
from rest_framework.response import Response

from .forms import DocumentForm
from .models import (
    Document, DocumentType, File)
from .serializers import (
    TempFileSerializer, ReadFileSerializer)
from materials.models import Material, Batch
from accounts.models import Account

class ReadFileView(
    mixins.CreateModelMixin,
    generics.GenericAPIView):
    serializer_class = ReadFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class TempFileView(
    mixins.CreateModelMixin,
    generics.GenericAPIView):
    serializer_class = TempFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        account = Account.objects.get(pk=self.request.user)
        serializer.save(creator=account)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class DocumentDetailView(LoginRequiredMixin, generic.DetailView):
    model = Document

    def get_context_data(self, **kwargs):
        context = super(DocumentDetailView, self).get_context_data(**kwargs)
        context['file'] = get_object_or_404(File, document=self.object)
        return context

class DocumentCreateView(LoginRequiredMixin, View):

    def default_view(self, request, form):
        # For rendering non-form document name/code fields
        account = Account.objects.get(pk=self.request.user)
        materials = Material.objects.filter(
            organization=account.active_organization
        ).order_by('code')

        # For populating JS document types array
        document_types = DocumentType.objects.all()

        return render(request, 'documents/document_create.html', {
            'form': form,
            'materials': materials,
            'document_types': document_types
        })

    def get(self, request):
        form = DocumentForm()
        return self.default_view(request, form)

    def post(self, request):
        form = DocumentForm(request.POST)
        if form.is_valid():
            account = get_object_or_404(Account, pk=self.request.user)
            material = get_object_or_404(Material, pk=form.cleaned_data['material_id'])
            document_type = form.cleaned_data['document_type']

            document = Document()
            document.creator = account
            document.organization = account.active_organization
            document.material = material
            document.document_type = document_type

            file = get_object_or_404(File, pk=form.cleaned_data['file_id'])
            file.document = document
            file.saved = datetime.now()

            if document_type.level == 'batch':
                batch = Batch(code=form.cleaned_data['batch_code'])
                batch.material = material
                document.batch = batch
                batch.save()

            document.save()
            file.save()

            print('hello world')

            return HttpResponseRedirect(
                reverse('documents:details', kwargs={'pk': document.id}))
        
        return self.default_view(request, form)

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