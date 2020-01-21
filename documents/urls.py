from django.urls import path

from . import views

app_name = 'documents'
api_prefix = 'api'
urlpatterns = [
  path('', views.documents, name='list'),
  path('create', views.DocumentCreateView.as_view(), name='create'),
  path('%s/create_file_presigned_url' % api_prefix,
    views.CreateFilePresignedURLView.as_view(),
    name='create_file_presigned_url'),




  path('inbox/', views.inbox, name='inbox'),
  path('sent/', views.sent, name='sent'),
  path('materials/', views.materials, name='materials'),
  path('colleagues/', views.colleagues, name='colleagues'),
  path('r/<str:file_to_render>', views.r),
]