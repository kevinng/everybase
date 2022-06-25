from django.urls import path
from leads import views

app_name = 'leads'
urlpatterns = [
    path('my', views.my_leads, name='my_leads'),
    path('create', views.lead_create, name='lead_create'),
    path('<int:id>', views.lead_detail, name='lead_detail'),
    path('contact/<int:id>', views.contact_detail, name='contact_detail'),
    path('<int:id>/contact', views.lead_capture, name='lead_capture'),
    path('<int:id>/success', views.lead_created_success, name='lead_created_success'),



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