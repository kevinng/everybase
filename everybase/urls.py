from everybase import settings

from relationships import views as relviews
from common import views as comviews
from leads import views as leviews

from django.contrib import admin
from django.urls import include, path
from django.conf.urls import include
from django.shortcuts import render

import sentry_sdk

def trigger_error(request):
    """View to test the logging of unhandled errors in Sentry"""
    division_by_zero = 1 / 0

def trigger_handled_error(request):
    """View to test the logging of handled errors in Sentry"""
    try:
        division_by_zero = 1 / 0
    except Exception as err:
        sentry_sdk.capture_exception(err)
    return render(request, 'chat/pages/error.html', {})

urlpatterns = [
    path('ads.txt', comviews.ads_txt, name='ads_txt'), # For Adsense and other ad networks
    path('', relviews.user_list, name='home'),
    path('login', relviews.log_in, name='login'),
    path('logout', relviews.log_out, name='logout'),
    path('register', relviews.register, name='register'),
    path('confirm-whatsapp-login', relviews.confirm_whatsapp_login, name='confirm_whatsapp_login'),

    path('status', relviews.status, name='status'),
    path('settings', relviews.profile_settings, name='profile_settings'),
    path('verify_whatsapp', relviews.verify_whatsapp, name='verify_whatsapp'),
    path('update_phone_number', relviews.update_phone_number, name='update_phone_number'),
    path('contacts', relviews.contacts, name='contacts'),
    path('lookup', relviews.lookup, name='lookup'),

    # path('common/', include('common.urls')),
    path('chat/', include('chat.urls')),
    path('users/', include('relationships.urls')),

    path(settings.ADMIN_PATH + '/', include('loginas.urls')),
    path(settings.ADMIN_PATH + '/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('sentry-debug', trigger_error), # trigger error
    path('sentry-debug-handled', trigger_handled_error), # handle error

    # path('ml/<uuid:uuid>/', relviews.magic_login, name='magic_login'),
    # path('confirm-email-login/', relviews.confirm_email_login, name='confirm_email_login'),
]

admin.site.site_title = "" # No title
admin.site.site_header = "Everybase Admin"
admin.site.index_title = "Welcome to Everybase Admin Portal"