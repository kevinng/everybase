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


    
    # Login and register
    path('login', relviews.log_in, name='login'),
    path('register', relviews.register, name='register'),
    path('confirm-whatsapp-login', relviews.confirm_whatsapp_login, name='confirm_whatsapp_login'),
    path('select-country', relviews.select_country, name='select-country'),
    path('verify-whatsapp', relviews.verify_whatsapp, name='verify_whatsapp'),

    # User menu and settings
    path('settings', relviews.profile_settings, name='profile_settings'),
    path('logout', relviews.log_out, name='logout'),
    path('update-phone-number', relviews.update_phone_number, name='update_phone_number'),
    path('update-requirements', relviews.requirements, name='update_requirements'),
    
    # Navigation bar
    path('', relviews.user_list, name='home'), # AKA search
    path('history', relviews.history, name='history'),
    path('lookup', relviews.lookup, name='lookup'),
    path('pricing', comviews.pricing, name='pricing'),
    path('earn-money', comviews.earn_money, name='earn_money'),
    path('faq', comviews.faq, name='faq'),

    # App URLs
    path('chat/', include('chat.urls')),
    path('users/', include('relationships.urls')),
    path('alerts/', include('relationships.alerts_urls')),

    # Administration
    path(settings.ADMIN_PATH + '/', include('loginas.urls')),
    path(settings.ADMIN_PATH + '/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('sentry-debug', trigger_error), # trigger error
    path('sentry-debug-handled', trigger_handled_error), # handle error
]

admin.site.site_title = "" # No title
admin.site.site_header = "Everybase Admin"
admin.site.index_title = "Welcome to Everybase Admin Portal"