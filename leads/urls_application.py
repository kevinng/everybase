from django.urls import path
from leads import views

app_name = 'applications'
urlpatterns = [
    path('<int:pk>', views.application_detail, name='application_detail'),
    path('my_leads', views.application_my_leads_list, name='application_my_leads_list'),
]