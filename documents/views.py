from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.views import View
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

class DocumentDetailView(LoginRequiredMixin, DetailView):
    model = Document

    def get_context_data(self, **kwargs):
        context = super(DocumentDetailView, self).get_context_data(**kwargs)
        context['file'] = get_object_or_404(File, document=self.object)
        return context

def document_view(request, form, template, additional_context={}):
    # For rendering non-form document name/code fields
    account = Account.objects.get(pk=request.user)
    materials = Material.objects.filter(
        organization=account.active_organization
    ).order_by('code')

    # For populating JS document types array
    document_types = DocumentType.objects.all()

    context = {
        'form': form,
        'materials': materials,
        'document_types': document_types
    }
    
    context.update(additional_context)
    return render(request, template, context)

def get_document(pk):

    document = get_object_or_404(Document, pk=pk)

    initial = {
        'document_type': document.document_type,
        'material_id': document.material.id,
        'file_id': document.files.all()[0].id
    }

    if document.batch != None and document.batch != '':
        initial['batch_code'] = document.batch.code

    form = DocumentForm(initial=initial)
    context = {'document': document}

    return (form, context)

class DocumentDeleteView(LoginRequiredMixin, View):

    def get(self, request, pk):
        (form, context) = get_document(pk)

        return document_view(
            request, form, 'documents/document_delete.html',
            additional_context=context)

    def post(self, request, pk):
        document = get_object_or_404(Document, pk=pk)
        document.deleted = datetime.now()
        document.save()
        return HttpResponseRedirect(reverse('documents:list'))

class DocumentEditView(LoginRequiredMixin, View):

    def get(self, request, pk):
        (form, context) = get_document(pk)

        return document_view(
            request, form, 'documents/document_edit.html',
            additional_context=context)
    
    def post(self, request, pk):
        form = DocumentForm(request.POST)
        if form.is_valid():
            document_type = form.cleaned_data['document_type']
            material = get_object_or_404(Material, pk=form.cleaned_data['material_id'])

            document = Document.objects.get(pk=pk)
            document.material = material
            document.document_type = document_type

            this_batch = document.batch

            if document_type.level == 'batch':
                batch_code = form.cleaned_data['batch_code']
                batches = Batch.objects\
                    .filter(material=material)\
                    .filter(code=batch_code)

                # If the batch we need exists, assign it. Otherwise, create it.
                if batches.exists() and this_batch.id != batches[0].id:
                    document.batch = batches[0]
                else:
                    new_batch = Batch(
                        code=batch_code,
                        material=material
                    )
                    document.batch = new_batch
                    new_batch.save()

            document.save()
            
            return HttpResponseRedirect(
                reverse('documents:details', kwargs={'pk': document.id}))
        
        return document_view(request, form, 'documents/document_edit.html')

class DocumentCreateView(LoginRequiredMixin, View):

    def get(self, request):
        form = DocumentForm()
        return document_view(request, form, 'documents/document_create.html')

    def post(self, request):
        form = DocumentForm(request.POST)
        if form.is_valid():
            account = get_object_or_404(Account, pk=self.request.user)
            material = get_object_or_404(Material, pk=form.cleaned_data['material_id'])
            document_type = form.cleaned_data['document_type']
            batch_code = form.cleaned_data['batch_code']

            document = Document()
            document.creator = account
            document.organization = account.active_organization
            document.material = material
            document.document_type = document_type

            file = get_object_or_404(File, pk=form.cleaned_data['file_id'])
            file.document = document
            file.saved = datetime.now()

            if document_type.level == 'batch':
                batches = Batch.objects\
                    .filter(material=material)\
                    .filter(code=batch_code)

                # If the batch we need exists, assign it. Otherwise, create it.
                if batches.exists():
                    document.batch = batches[0]
                else:
                    batch = Batch(code=batch_code)
                    batch.material = material
                    document.batch = batch
                    batch.save()

            document.save()
            file.save()

            return HttpResponseRedirect(
                reverse('documents:details', kwargs={'pk': document.id}))
        
        return document_view(request, form, 'documents/document_create.html')

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

def rj(request, file_to_render):
    template_name = 'documents/js/%s' % file_to_render
    return TemplateResponse(request, template_name, {})