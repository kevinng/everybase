from django.urls import path
from leads import views

app_name = 'products'
urlpatterns = [
    # Don't map slug URLs above generic links like lead_create. Otherwise,
    # 'products/create' will go to a lead detail page with slug 'create'.
    path('', views.product_list, name='product_list'),
    path('my', views.my_products, name='my_products'),
    path('create', views.product_create, name='product_create'),
    path('<slug:slug>', views.product_detail, name='product_detail'),
]