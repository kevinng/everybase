from django.urls import path
from leads import views

app_name = 'leads'
urlpatterns = [
    path('my', views.my_leads, name='my_leads'),
    path('create', views.lead_create, name='lead_create'),
    path('<int:id>', views.lead_detail, name='lead_detail'),
    path('contact/<int:id>/notes', views.contact_detail_private_notes, name='contact_detail_private_notes'),
    path('contact/<int:id>/other', views.contact_detail_other_contacts, name='contact_detail_other_contacts'),
    path('<int:id>/contact', views.contact_lead, name='contact_lead'),
    path('<int:id>/success', views.lead_created_success, name='lead_created_success'),
    path('<int:id>/wechat', views.redirect_contact_wechat, name='redirect_contact_wechat'),
    path('<int:id>/whatsapp', views.redirect_contact_whatsapp, name='redirect_contact_whatsapp')


# path('', views.lead_list, name='lead_list'),
# TODO: I should have another page for an isolated contact form for sharing as well

    

    
    

    # NOTE: map other routes above slug routes
    # path('<slug:slug>', views.lead_detail, name='lead_detail'),


    # path('<slug:slug>/edit', views.lead_edit, name='lead_edit'),
    # path('<slug:slug>/delete', views.lead_delete, name='lead_delete'),

    # path('<slug:slug>/edit', views.lead_edit, name='lead_edit'),
    
    # Pre v5 routings
    # path('<slug:slug>/applications', views.LeadApplicationListView.as_view(), name='lead_applications'),
]