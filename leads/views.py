import json

from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.urls import reverse
from django.shortcuts import render

from leads import serializers, models, forms
from files import views as fiviews, models as fimods

class LeadListView(ListView):
    model = models.Lead
    paginate_by = 18

def create_lead(request):
    if request.method == 'POST':
        form = forms.LeadForm(request.POST)
        if form.is_valid():
            lead = models.Lead.objects.create(
                title=form.cleaned_data.get('title'),
                details=form.cleaned_data.get('details'),
                lead_type=form.cleaned_data.get('lead_type'),
                author_type=form.cleaned_data.get('author_type'),
                country_string=form.cleaned_data.get('country_string'),
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
            
            # TODO: redirect to lead details page
            return HttpResponseRedirect(reverse('leads:list'))
    else:
        form = forms.LeadForm()

    return render(request, 'leads/create_lead.html', {'form': form})

# @csrf_exempt
class WriteOnlyPresignedURLView(fiviews.WriteOnlyPresignedURLView):
    serializer_class = serializers.WriteOnlyPresignedURLSerializer