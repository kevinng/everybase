from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.response import TemplateResponse # Remove
from django.shortcuts import render, get_object_or_404
from django.views import View, generic
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse

from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions

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

def document_view(request, form, template, additional_context={}):
    # For rendering non-form document name/code fields
    account = Account.objects.get(pk=request.user)
    materials = Material.objects.filter(
        organization=account.active_organization
    ).order_by('code')

    # For populating JS document types array
    document_types = DocumentType.objects.all()

    if form == None:
        form = DocumentForm(initial={
            'document_type': document_types[0],
            'material_id': materials[0].id
        })

    context = {
        'form': form,
        'materials': materials,
        'document_types': document_types
    }
    
    context.update(additional_context)
    return render(request, template, context)

def get_document_view(pk, request, template):
    document = get_object_or_404(Document, pk=pk)
    if document.deleted != None:
        raise Http404("Document does not exist.")

    initial = {
        'document_type': document.document_type,
        'material_id': document.material.id,
        'file_id': document.files.all()[0].id
    }

    if document.batch != None:
        initial['batch_code'] = document.batch.code

    form = DocumentForm(initial=initial)
    context = {'document': document}

    return document_view(request, form, template, additional_context=context)

class DocumentDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        return get_document_view(pk, request, 'documents/document_detail.html')

class DocumentDeleteView(LoginRequiredMixin, View):

    def get(self, request, pk):
        return get_document_view(pk, request, 'documents/document_delete.html')

    def post(self, request, pk):
        document = get_object_or_404(Document, pk=pk)
        document.deleted = datetime.now()
        document.save()
        return HttpResponseRedirect(reverse('documents:list'))

class DocumentEditView(LoginRequiredMixin, View):

    def get(self, request, pk):
        return get_document_view(pk, request, 'documents/document_edit.html')
    
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
        return document_view(request, None, 'documents/document_create.html')

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

class DocumentListView(LoginRequiredMixin, generic.ListView):
    model = Document
    paginate_by = 36

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['document_types'] = DocumentType.objects.all().order_by('-name')
        return context

    def get_queryset(self):
        material_name = self.request.GET.get('material_name', None)
        material_code = self.request.GET.get('material_code', None)
        batch_code = self.request.GET.get('batch_code', None)
        created_start_date = self.request.GET.get('created_start_date', None)
        created_end_date = self.request.GET.get('created_end_date', None)

        documents = Document.objects.order_by('-created')

        if material_name != None and material_name != '':
            documents = documents.filter(material__name__icontains=material_name)
        
        if material_code != None and material_code != '':
            documents = documents.filter(material__code__icontains=material_code)

        if batch_code != None and batch_code != '':
            documents = documents.filter(batch__code__icontains=batch_code)

        if created_start_date != None and created_start_date != '':
            (month, day, year) = map(lambda x: int(x), created_start_date.split('/'))
            start_date = datetime(year, month, day)
        else:
            start_date = None

        if created_end_date != None and created_end_date != '':
            (month, day, year) = map(lambda x: int(x), created_end_date.split('/'))
            end_date = datetime(year, month, day)
        else:
            end_date = None
        
        if start_date != None and end_date != None:
            documents = Document.objects.filter(created__range=(start_date, end_date))
        elif start_date != None and end_date == None:
            documents = Document.objects.filter(created__gt=start_date)
        elif start_date == None and end_date != None:
            documents = Document.objects.filter(created__lt=end_date)
        
        return documents

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