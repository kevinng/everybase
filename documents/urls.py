from django.urls import path

from . import views

app_name = 'documents'
api_prefix = 'api'
urlpatterns = [
  path('', views.documents, name='list'),
  path('create', views.DocumentCreateView.as_view(), name='create'),
  path('details/<uuid:pk>', views.DocumentDetailView.as_view(), name='details'),
  path('%s/temp_file' % api_prefix, views.TempFileView.as_view(), name='temp_file'),
  path('%s/read_file' % api_prefix, views.ReadFileView.as_view(), name='read_file'),




  path('inbox/', views.inbox, name='inbox'),
  path('sent/', views.sent, name='sent'),
  path('materials/', views.materials, name='materials'),
  path('colleagues/', views.colleagues, name='colleagues'),
  path('r/<str:file_to_render>', views.r),
]