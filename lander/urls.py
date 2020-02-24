from django.urls import path
from . import views

urlpatterns = [
  path('', views.slow_moving_stock, name='index')
]