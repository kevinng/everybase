from django.urls import path
from leads import views

app_name = 'leads'
urlpatterns = [
    # Don't map slug URLs above generic links like lead_create. Otherwise,
    # 'leads/create' will go to a lead detail page with slug 'create'.
    path('', views.lead_list, name='lead_list'),
    path('create', views.lead_create, name='lead_create'),
    path('<slug:slug>', views.lead_detail, name='lead_detail'),
    path('<slug:slug>/edit', views.lead_edit, name='lead_edit'),
    path('<slug:slug>/applications', views.LeadApplicationListView.as_view(), name='lead_applications'),
    path('applications/<int:aid>', views.application_detail, name='application_detail'),
]