from django.urls import path
from . import views

urlpatterns = [
  path('', views.ex_stock, name='index')
]