"""Map to URL root. Namespace to be configured at root."""

from django.urls import path
from . import views

app_name = 'chat__root__pay'
urlpatterns = [
    path('pay/<str:id>/', views.redirect_checkout_page, name='payment')
]