from django.urls import path
from relationships import views

app_name = 'users'
urlpatterns = [
    path('settings', views.profile_settings, name='settings'),
    path('verify_whatsapp', views.verify_whatsapp, name='verify_whatsapp'),
    path('disable_whatsapp', views.disable_whatsapp, name='disable_whatsapp'),

    # path('change_password', views.change_password, name='change_password'),

    path('m/<str:file_to_render>', views.m),

    # Pre v5 routes
    # path('', views.user_list, name='user_list'),
    #
    # NOTE: Map slug routes after '' route
    # path('<slug:slug>', views.user_detail_lead_list, name='user_detail'),
    # path('<slug:slug>/leads', views.UserLeadListView.as_view(), name='user_leads'),
    # path('<slug:slug>/edit', views.user_edit, name='user_edit'),
]