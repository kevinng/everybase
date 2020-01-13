from django.urls import path

from . import views

urlpatterns = [
  path('inbox/', views.inbox, name='inbox'),
  path('documents/', views.documents, name='documents'),
  path('sent/', views.sent, name='sent'),
  path('materials/', views.materials, name='materials'),
  path('colleagues/', views.colleagues, name='colleagues'),
  path('r/<str:file_to_render>', views.r),
]