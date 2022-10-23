from django.urls import path
from relationships import views

app_name = 'users'
urlpatterns = [
    path('upload_status_file/<int:user_id>',
        views.upload_status_file,
        name='upload_status_file'),
    path('delete_status_file/<int:user_id>',
        views.delete_status_file,
        name='delete_status_file'),
    path('clear_abandoned_files/<int:user_id>',
        views.clear_abandoned_files,
        name='clear_abandoned_files'),
    path('settings',
        views.users__settings,
        name='settings'),
    path('resend-email-code/<int:user_id>',
        views.users__settings__resend_email_code,
        name='resend_email_code'),
    path('confirm_email',
        views.users__settings__confirm_email,
        name='confirm_email'),
    path('upload_review_file/<int:reviewer_id>/<int:phone_number_id>',
        views.upload_review_file,
        name='upload_review_file'),
    path('delete_review_file',
        views.delete_review_file,
        name='delete_review_file'),
]