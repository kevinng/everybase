"""URLs to be mapped to URL root"""

from django.urls import path
from . import views

app_name = 'chat_root'
urlpatterns = [
    path('wa/<str:id>/', views.redirect_whatsapp_phone_number, name='whatsapp'),
    # path('pay/<str:id>/', views.redirect_checkout_page, name='payment')
]