from django.urls import path
from leads import views

app_name = 'applications'
urlpatterns = [
    path('<int:pk>', views.application_detail, name='application_detail'),
    path('for_my_leads', views.application_for_my_leads_list, name='application_for_my_leads_list'),
    path('from_me_as_an_agent', views.application_from_me_as_an_agent_list, name='application_from_me_as_an_agent_list'),
]