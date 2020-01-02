from django.urls import include, path

from . import views

urlpatterns = [
  path('login/', views.login, name='login'),
  path('logout/', views.logout, name='logout'),
  path('reset_password/', views.reset_password, name='reset_password'),
  path('set_password/', views.set_password, name='set_password_post'),
  path('set_password/<uuid:code>', views.set_password, name='set_password'),
  path('send_sample_email', views.send_sample_email),
  path('accounts/r/<str:file_to_render>', views.r),
]