from django.http import HttpResponseRedirect

from django.template.response import TemplateResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from accounts.models import Account
from materials.models import Material
from .forms import MaterialForm

class MaterialDetailView(generic.DetailView):
    model = Material

class MaterialListView(generic.ListView):
    model = Material
    paginate_by = 36

    def get_queryset(self):
        code = self.request.GET.get('code', None)
        name = self.request.GET.get('name', None)

        materials = Material.objects.order_by('-name')
        if code != None and code != '':
            materials = materials.filter(code__contains=code)
        
        if name != None and name != '':
            materials = materials.filter(name__contains=name)

        return materials

def material_create(request):
    if request.method == 'POST':
        account = Account.objects.get(pk=request.user)
        if account.active_organization == None:
            # Material created must tie to active organization.
            return render(request, 'errors/access_denied.html')

        form = MaterialForm(request.POST)
        if form.is_valid():

            Material(
                name=form.cleaned_data['name'],
                code=form.cleaned_data['code'],
                organization=account.active_organization
            ).save()

            return HttpResponseRedirect(reverse('materials:list'))
    else:
        form = MaterialForm()

    return render(request, 'materials/material_create.html', {'form': form})

def r(request, file_to_render):
    template_name = 'materials/%s' % file_to_render
    return TemplateResponse(request, template_name, {})