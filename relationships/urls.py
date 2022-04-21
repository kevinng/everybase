from django.urls import path
from relationships import views

app_name = 'users'
urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('<slug:slug>', views.user_detail_lead_list, name='user_detail'),
    path('<slug:slug>/leads', views.UserLeadListView.as_view(), name='user_leads'),
    path('<slug:slug>/edit', views.user_edit, name='user_edit'),
]