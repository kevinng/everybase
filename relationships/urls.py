from django.urls import path
from relationships import views

app_name = 'users'
urlpatterns = [
    path('<uuid:uuid>', views.suggestions, name='user_detail'),
    path('<uuid:uuid>/reviews', views.user_detail, name='user_detail'),

    # path('m/<str:file_to_render>', views.m),

    # NOTE: Map slug routes after '' route
    # path('<slug:slug>', views.user_detail_lead_list, name='user_detail'),
    # path('<slug:slug>/leads', views.UserLeadListView.as_view(), name='user_leads'),
    # path('<slug:slug>/edit', views.user_edit, name='user_edit'),
]