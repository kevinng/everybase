from django.urls import path
from relationships import views

app_name = 'relationships'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('confirm_register/<str:user_uuid>', views.confirm_register,
        name='confirm_register'),
    path('is_registered/<str:user_uuid>', views.is_registered,
        name='is_registered'),
    path('login/', views.log_in, name='login'),
    path('confirm_login/<str:user_uuid>', views.confirm_login,
        name='confirm_login'),
    path('is_logged_in/<str:user_uuid>', views.is_logged_in,
        name='is_logged_in'),
    path('logout/', views.log_out, name='logout')
]