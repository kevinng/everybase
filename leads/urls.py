from django.urls import path
from leads import views

app_name = 'leads'
urlpatterns = [
    path('', views.LeadListView.as_view(), name='lead_list'),
    path('<int:pk>', views.lead_detail, name='lead_detail'),
    path('create', views.lead_create, name='lead_create'),
    path('edit/<int:pk>', views.lead_edit, name='lead_edit'),
    path('<int:pk>/save', views.toggle_save_lead, name='toggle_save_lead')
]