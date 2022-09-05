from django.urls import path
from leads import views

app_name = 'leads'
urlpatterns = [
    # path('<int:id>/whatsapp', views.redirect_contact_whatsapp, name='redirect_contact_whatsapp'),

    # NOTE: map other routes above slug routes
    # path('<slug:slug>', views.lead_detail, name='lead_detail'),

    # path('<slug:slug>/edit', views.lead_edit, name='lead_edit'),
    # path('<slug:slug>/delete', views.lead_delete, name='lead_delete'),

    # path('<slug:slug>/edit', views.lead_edit, name='lead_edit'),
    
    # Pre v5 routings
    # path('<slug:slug>/applications', views.LeadApplicationListView.as_view(), name='lead_applications'),
]