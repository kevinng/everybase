from django.urls import path
from leads import views

app_name = 'leads'
urlpatterns = [
    path('create/', views.create_lead, name='create'),
    path('write_only_presigned_url/',
        views.WriteOnlyPresignedURLView.as_view(),
        name='write_only_presigned_url'),
    path('<str:uuid>/', views.lead_detail, name='detail')
]