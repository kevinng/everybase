from django.urls import path
from leads import views

app_name = 'leads'
urlpatterns = [
    # Don't map slug URLs above generic links like lead_create. Otherwise,
    # 'leads/create' will go to a lead detail page with slug 'create'.
    path('', views.lead_list, name='lead_list'),
    path('create', views.lead_create, name='lead_create'),
    path('edit/<slug:slug>', views.lead_edit, name='lead_edit'),
    path('<slug:slug>/save', views.toggle_save_lead, name='toggle_save_lead'),
    path('<slug:slug>', views.lead_detail, name='lead_detail'),
]