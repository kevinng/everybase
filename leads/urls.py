from django.urls import path
from leads import views

app_name = 'leads'
urlpatterns = [
    path('create/', views.create_lead, name='create'),
    path('write_only_presigned_url/',
        views.WriteOnlyPresignedURLView.as_view(),
        name='write_only_presigned_url'),

# Create a URL to delete a file


    # path('<str:id>/', views.LeadDetailView.as_view(), name='detail'),
    # path('<str:id>/update/', views.LeadUpdateView.as_view(), name='update'), # use new lead page as an example
    # path('<str:id>/contact/', views.contact_lead_owner, name='contact_lead_owner'), # contact lead owner
    # path('<str:id>/save/', views.save_lead, name='save_lead'), # save/unsave lead
    # path('saved/', views.SavedLeadListView, name='saved_leads'), # saved leads
]