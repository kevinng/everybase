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

    path('', leviews.lead_list, name='home'),
    path('login/', relviews.log_in, name='login'),
    path('logout/', relviews.log_out, name='logout'),
    path('register/', relviews.register, name='register'),
    path('confirm-whatsapp-login/', relviews.confirm_whatsapp_login, name='confirm_whatsapp_login'),
    path('confirm-email-login/', relviews.confirm_email_login, name='confirm_email_login'),
    path('ml/<uuid:uuid>/', relviews.magic_login, name='magic_login'),

    path('common/', include('common.urls')),
    path('chat/', include('chat.urls')),
    path('leads/', include('leads.urls')),
    path('users/', include('relationships.urls')),

    path(settings.ADMIN_PATH + '/', include('loginas.urls')),
    path(settings.ADMIN_PATH + '/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('sentry-debug/', trigger_error), # trigger error
    path('sentry-debug-handled/', trigger_handled_error), # handle error







    # NEED TO CHANGE THIS TO LANDING PAGE



    # OLD LINKS
    


    # Common
    # path('', comviews.home, name='home'),

    # path('', leviews.lead_list, name='lead_list'),

    # Leads
    # path('applications/', include('leads.urls_application')),
    
    # Relationships
    
    # path('confirm-login/', relviews.confirm_login, name='confirm_login'),

    # path('confirm-phone/', relviews.confirm_phone, name='confirm_email'),

    # Chat

    # Files
    # path('files/', include('files.urls')),

    # Django admin obfuscated URL

    # Django Rest Framework login

    # Pre v5 routings
    # path('', comviews.home, name='home'),
    # path('pricing', comviews.pricing, name='pricing'),
    #
    # path('register/', relviews.register, name='register'),
    # path('confirm_register/<str:user_uuid>', relviews.confirm_register,
    #     name='confirm_register'),
    # path('is_registered/<str:user_uuid>', relviews.is_registered,
    #     name='is_registered'),
    # path('login/', relviews.log_in, name='login'),
    # path('confirm_login/<str:user_uuid>', relviews.confirm_login,
    #     name='confirm_login'),
    # path('is_logged_in/<str:user_uuid>', relviews.is_logged_in,
    #     name='is_logged_in'),
    # path('logout/', relviews.log_out, name='logout'),
    # path('persons/', include('relationships.urls')),
]

admin.site.site_title = "" # No title
admin.site.site_header = "Everybase Admin"
admin.site.index_title = "Welcome to Everybase Admin Portal"