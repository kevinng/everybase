from django.urls import path
from relationships import views

app_name = 'users'
urlpatterns = [
    path('<int:pk>/comments', views.user_comments, name='user_comments'),
    path('<int:pk>/leads', views.UserLeadListView.as_view(), name='user_leads'),
    path('<int:pk>/whatsapp', views.whatsapp, name='whatsapp')
]