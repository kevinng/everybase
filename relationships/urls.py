from django.urls import path
from relationships import views

app_name = 'users'
urlpatterns = [
    path('settings', views.profile_settings, name='settings'),
    path('verify_whatsapp', views.verify_whatsapp, name='verify_whatsapp'),
    path('disable_whatsapp', views.disable_whatsapp, name='disable_whatsapp'),
    path('update_email', views.update_email, name='update_email'),
    path('update_phone_number', views.update_phone_number, name='update_phone_number'),

    path('<uuid:uuid>', views.user_detail, name='user_detail'),

    # NO following, only friends.
    path('<uuid:uuid>/following', views.user_detail__following, name='following'),
    # path('<uuid:uuid>/followers', views.user_detail, name='user_detail__followers'),
    path('<uuid:uuid>/contacted', views.user_detail__contacted, name='contacted'),
    path('<uuid:uuid>/reviews', views.user_detail__reviews, name='reviews'),

    path('<uuid:uuid>/friends', views.user_detail__friends, name='friends'),

    path('<uuid:uuid>/requests', views.friend_requests, name='requests'),

    # path('change_password', views.change_password, name='change_password'),

    # path('m/<str:file_to_render>', views.m),

    # Pre v5 routes
    # path('', views.user_list, name='user_list'),
    #
    # NOTE: Map slug routes after '' route
    # path('<slug:slug>', views.user_detail_lead_list, name='user_detail'),
    # path('<slug:slug>/leads', views.UserLeadListView.as_view(), name='user_leads'),
    # path('<slug:slug>/edit', views.user_edit, name='user_edit'),
]