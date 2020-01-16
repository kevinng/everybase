from django.urls import path

from . import views

app_name = 'materials'
urlpatterns = [
  path('', views.material_list, name='list'),
  path('create/', views.material_create, name='create'),
  path('r/<str:file_to_render>', views.r)
]