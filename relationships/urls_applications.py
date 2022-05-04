from django.urls import path
from relationships import views

app_name = 'applications'
urlpatterns = [
    path('', views.application_list, name='application_list'),
    path('<int:pk>', views.application_detail, name='application_detail'),
]