from django.urls import path

from . import views

app_name = 'documents'
urlpatterns = [
  path('', views.documents, name='list'),

  path('inbox/', views.inbox, name='inbox'),
  path('sent/', views.sent, name='sent'),
  path('materials/', views.materials, name='materials'),
  path('colleagues/', views.colleagues, name='colleagues'),
  path('r/<str:file_to_render>', views.r),
]