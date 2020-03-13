from django.urls import path

from . import views

app_name = 'materials'
urlpatterns = [
  path('', views.MaterialListView.as_view(), name='list'),
  path('details/<uuid:pk>', views.MaterialDetailView.as_view(), name='details'),
  path('edit/<uuid:pk>', views.MaterialEditView.as_view(), name='edit'),
  path('create/', views.MaterialCreateView.as_view(), name='create'),
  path('delete/<uuid:pk>', views.MaterialDeleteView.as_view(), name='delete'),
  path('r/<str:file_to_render>', views.r)
]