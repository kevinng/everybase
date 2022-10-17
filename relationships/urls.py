from django.urls import path
from relationships import views

app_name = 'users'
urlpatterns = [
    path('upload_status_file/<int:user_id>/',
        views.upload_status_file,
        name='upload_status_file'),
    path('delete_status_file/<int:user_id>/',
        views.delete_status_file,
        name='delete_status_file'),
    path('delete_orphan_files/<int:user_id>/',
        views.delete_orphan_files,
        name='delete_orphan_files'),
    path('settings',
        views.users__settings,
        name='settings'),
    path('resend-email-code/<int:user_id>/',
        views.users__settings__resend_email_code,
        name='resend_email_code'),
    path('confirm_email',
        views.users__settings__confirm_email,
        name='confirm_email')
]