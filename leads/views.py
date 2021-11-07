from django.views.generic.list import ListView
from django.shortcuts import render

from . import models

class LeadListView(ListView):
    model = models.Lead
    paginate_by = 18

def create_lead(request):
    
    return render(request, 'leads/new_lead.html', {})