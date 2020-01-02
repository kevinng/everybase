from django.urls import path

from . import views

urlpatterns = [
  path('r/<str:file_to_render>', views.r),
]