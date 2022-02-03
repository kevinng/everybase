from django.urls import path
from relationships import views

app_name = 'relationships'
urlpatterns = [
    path('users/<int:pk>/comments', views.user_comments, name='user_comments'),
    path('users/<int:pk>/leads', views.UserLeadListView.as_view(), name='user_leads'),
    path('users/<int:pk>/whatsapp', views.whatsapp, name='whatsapp'),
    path('register/', views.register, name='register'),
    path('register_link/<str:user_uuid>', views.register_link, name='register_link'),
    path('confirm_register/<str:user_uuid>', views.confirm_register, name='confirm_register'),
    path('login/', views.log_in, name='login'),
    path('login_link/<str:user_uuid>', views.log_in_link, name='login_link'),
    path('confirm_login/<str:user_uuid>', views.confirm_log_in, name='confirm_login'),
    path('logout/', views.log_out, name='logout')
]