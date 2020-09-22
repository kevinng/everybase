from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
  path('lists/<str:products_list_id>', views.products, name='enquiry'),
  path('thanks', views.thanks, name='thanks')
]