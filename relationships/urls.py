from django.urls import path
from relationships import views

app_name = 'users'
urlpatterns = [
    # Pre v5 routes
    # path('', views.user_list, name='user_list'),

    # Superio routes
    path('profile', views.profile, name='profile'),
    path('messages', views.messages, name='messages'),

    # Pre v5 routes
    # Map slug routes last
    # path('<slug:slug>', views.user_detail_lead_list, name='user_detail'),
    # path('<slug:slug>/leads', views.UserLeadListView.as_view(), name='user_leads'),
    # path('<slug:slug>/edit', views.user_edit, name='user_edit'),
]