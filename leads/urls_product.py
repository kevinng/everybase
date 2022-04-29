from django.urls import path
from leads import views

app_name = 'products'
urlpatterns = [
    # Don't map slug URLs above generic links like lead_create. Otherwise,
    # 'products/create' will go to a lead detail page with slug 'create'.
    path('', views.product_list, name='product_list'),
]