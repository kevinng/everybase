from django.urls import path
from relationships import views

app_name = 'register'
urlpatterns = [
    path('',
        views.register__enter_whatsapp,
        name='start'),
    path('select-country/<int:user_id>',
        views.register__select_country,
        name='select_country'),
    path('confirm-whatsapp/<int:user_id>',
        views.register__confirm_whatsapp,
        name='confirm_whatsapp'),
    path('resend-whatsapp-code/<int:user_id>',
        views.register__resend_whatsapp_code,
        name='resend_whatsapp_code'),
    path('enter-profile/<int:user_id>',
        views.register__enter_profile,
        name='enter_profile'),
    path('confirm-email/<int:user_id>',
        views.register__confirm_email,
        name='confirm_email'),
    path('resend-email-code/<int:user_id>',
        views.register__resend_email_code,
        name='resend_email_code'),
    path('enter-status/<int:user_id>',
        views.register__enter_status,
        name='enter_status')
]