from django.urls import path
from leads import views

app_name = 'leads'
urlpatterns = [
    path('', views.lead_list, name='lead_list'),
    path('my', views.my_leads, name='my_leads'),
    path('create', views.lead_create, name='lead_create'),

    # NOTE: map other routes above slug routes
    path('<slug:slug>', views.lead_detail, name='lead_detail'),
    path('<slug:slug>/delete', views.lead_delete, name='lead_delete'),

    # path('<slug:slug>/edit', views.lead_edit, name='lead_edit'),
    
    # Pre v5 routings
    # path('<slug:slug>/applications', views.LeadApplicationListView.as_view(), name='lead_applications'),
]