from django.urls import path
from leads import views

app_name = 'leads'
urlpatterns = [
    path('', views.LeadListView.as_view(), name='lead_list'),
    path('create', views.lead_create, name='lead_create'),
    path('edit/<int:pk>', views.LeadEdit.as_view(), name='lead_edit'),
    path('<int:pk>', views.LeadDetail.as_view(), name='lead_detail'),

    # Old routings
    # path('create/', views.create_lead, name='create'),
    # path('write_only_presigned_url/',
    #     views.WriteOnlyPresignedURLView.as_view(),
    #     name='write_only_presigned_url'),
    # path('<str:uuid>/', views.lead_detail, name='detail')
]