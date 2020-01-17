from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.response import TemplateResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    UpdateView, DetailView, ListView, DeleteView, CreateView)

from accounts.models import Account
from materials.models import Material
from .forms import MaterialForm

class MaterialEditView(LoginRequiredMixin, UpdateView):
    model = Material
    fields = ['name', 'code']
    template_name = 'materials/material_edit.html'

class MaterialDetailView(LoginRequiredMixin, DetailView):
    model = Material

class MaterialListView(LoginRequiredMixin, ListView):
    model = Material
    paginate_by = 36

    def get_queryset(self):
        code = self.request.GET.get('code', None)
        name = self.request.GET.get('name', None)

        materials = Material.objects.order_by('-name')
        if code != None and code != '':
            materials = materials.filter(code__icontains=code)
        
        if name != None and name != '':
            materials = materials.filter(name__icontains=name)

        return materials

class MaterialDeleteView(LoginRequiredMixin, DeleteView):
    model = Material
    success_url = reverse_lazy('materials:list')

class MaterialCreateView(LoginRequiredMixin, CreateView):
    model = Material
    fields = ['name', 'code']
    template_name = 'materials/material_create.html'

    def form_valid(self, form):
        account = Account.objects.get(pk=self.request.user)
        form.instance.organization = account.active_organization
        return super().form_valid(form)

def r(request, file_to_render):
    template_name = 'materials/%s' % file_to_render
    return TemplateResponse(request, template_name, {})