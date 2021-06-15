"""URLs to be mapped to the root of the application"""

from django.urls import path
from . import views

app_name = 'chat'
urlpatterns = [
    path('wa/<str:id>/', views.redirect_whatsapp_phone_number, name='whatsapp'),
]