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
    # For Adsense and other ad networks.
    path('ads.txt', comviews.ads_txt, name='ads_txt'),

    # Privacy and terms
    path('privacy', comviews.privacy, name='privacy'),
    path('terms', comviews.terms, name='terms'),

    path('', comviews.home, name='home'),
    path('login', relviews.log_in, name='login'),
    path('logout', relviews.log_out, name='logout'),

    path('lookup', relviews.lookup, name='lookup'),

    path('p/<str:phone_number>', relviews.user_detail, name='user_detail'),
    path('r/<str:phone_number>', relviews.user_reviews, name='user_reviews'),
    path('r/<str:phone_number>/new', relviews.review_create,
        name='review_create'),
    path('r/<str:reviewee_phone_number>/<str:reviewer_phone_number>',
        relviews.review_detail, name='review_detail'),
    path('w/<str:phone_number>', relviews.user_whatsapp, name='user_whatsapp'),

    path('users/', include('relationships.urls')),
    path('register/', include('relationships.urls_register')),
    path('login/', include('relationships.urls_login')),

    # App URLs
    # path('common/', include('common.urls')),
    path('chat/', include('chat.urls')),

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