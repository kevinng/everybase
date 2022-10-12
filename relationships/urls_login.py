from django.urls import path
from relationships import views

app_name = 'login'
urlpatterns = [
    path('', views.log_in, name='login'),
    path('<int:user_id>/confirm', views.confirm_whatsapp_login, name='confirm'),
]