from django.views.generic.list import ListView

from . import models

class LeadListView(ListView):
    model = models.Lead
    paginate_by = 18

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)