from django.urls import path
from relationships import views

app_name = 'users'
urlpatterns = [
    path('persons', views.user_list, name='user_list'),
    path('<slug:slug>', views.user_detail, name='user_detail'),
    path('<slug:slug>/leads', views.UserLeadListView.as_view(), name='user_leads'),
    path('<slug:slug>/whatsapp', views.whatsapp, name='whatsapp'),
    path('<slug:slug>/edit', views.user_edit, name='user_edit'),
    path('<slug:slug>/save', views.toggle_save_user, name='toggle_save_user')
]