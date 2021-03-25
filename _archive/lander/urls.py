from django.urls import path
from . import views

app_name = 'lander'
urlpatterns = [
  path('', views.home, name='home'),
  path('products', views.products, name='products'),
  path('services', views.services, name='services'),
  path('network', views.network, name='network'),
]