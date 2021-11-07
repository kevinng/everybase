from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'leads'
urlpatterns = [
    # path('<str:id>/', views.LeadDetailView.as_view(), name='detail'),
    path('create/', views.create_lead, name='create'),
    # path('<str:id>/update/', views.LeadUpdateView.as_view(), name='update'), # use new lead page as an example
    # path('<str:id>/contact/', views.contact_lead_owner, name='contact_lead_owner'), # contact lead owner
    # path('<str:id>/save/', views.save_lead, name='save_lead'), # save/unsave lead
    # path('saved/', views.SavedLeadListView, name='saved_leads'), # saved leads
]