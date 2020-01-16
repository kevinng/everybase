from django.urls import path

from . import views

app_name = 'materials'
urlpatterns = [
  path('', views.MaterialListView.as_view(), name='list'),
  path('create/', views.material_create, name='create'),
  path('r/<str:file_to_render>', views.r)
]