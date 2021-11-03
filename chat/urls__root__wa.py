"""Map to URL root. Namespace to be configured at root."""

from django.urls import path
from . import views

app_name = 'chat__root__wa'
urlpatterns = [
    path('<str:id>/', views.redirect_whatsapp_phone_number, name='whatsapp')
]