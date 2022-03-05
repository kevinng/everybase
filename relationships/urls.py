from django.urls import path
from relationships import views
from leads import views as leviews

app_name = 'users'
urlpatterns = [
    path('agents', leviews.AgentListView.as_view(), name='agent_list'),
    path('<int:pk>', views.user_comments, name='user_detail'),
    path('<int:pk>/comments', views.user_comments, name='user_comments'),
    path('<int:pk>/leads', views.UserLeadListView.as_view(), name='user_leads'),
    path('<int:pk>/whatsapp', views.whatsapp, name='whatsapp'),
    path('<int:pk>/edit', views.user_edit, name='user_edit'),
    path('<int:pk>/save', views.toggle_save_user, name='toggle_save_user')
]