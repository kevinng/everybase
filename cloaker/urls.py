from django.urls import path
from . import views

app_name = 'cloaker'
urlpatterns = [
  path('', views.iframe, name='iframe'),
  path('r/<str:file_to_render>', views.r),
]