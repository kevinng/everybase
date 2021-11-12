import json

from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.urls import reverse
from django.shortcuts import render
from django.contrib import messages

from leads import serializers, models, forms
from files import views as fiviews, models as fimods
from common import models as commods

class LeadListView(ListView):
    model = models.Lead
    paginate_by = 30

def create_lead(request):
    if request.method == 'POST':
        form = forms.LeadForm(request.POST)
        if form.is_valid():
            lead = models.Lead.objects.create(
                author=request.user.user,
                title=form.cleaned_data.get('title'),
                details=form.cleaned_data.get('details'),
                lead_type=form.cleaned_data.get('lead_type'),
                author_type=form.cleaned_data.get('author_type'),
                country=commods.Country.objects.get(
                    programmatic_key=form.cleaned_data.get('country')),
                commission_pct=form.cleaned_data.get('commission_pct'),
                commission_payable_after=form.cleaned_data.\
                    get('commission_payable_after'),
                commission_payable_after_others=form.cleaned_data.\
                    get('commission_payable_after_others'),
                other_commission_details=form.cleaned_data.\
                    get('other_commission_details')
            )

            # Associate file with lead
            file_datas = json.loads(form.cleaned_data.get('files'))
            for file_data in file_datas:
                uuid, _, filename = file_data
                file = fimods.File.objects.get(uuid=uuid)
                file.lead = lead
                file.filename = filename
                file.save()
            
            # TODO: add URL to lead details
            messages.info(request, 'Your lead has been posted.')

            return HttpResponseRedirect(reverse('leads__root:list'))
    else:
        form = forms.LeadForm()

    countries = commods.Country.objects.order_by('name')

    return render(request, 'leads/create_lead.html', {
        'form': form,
        'countries': countries
    })

# @csrf_exempt
class WriteOnlyPresignedURLView(fiviews.WriteOnlyPresignedURLView):
    serializer_class = serializers.WriteOnlyPresignedURLSerializer