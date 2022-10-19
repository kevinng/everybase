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
    path('privacy/', comviews.privacy, name='privacy'),
    path('terms/', comviews.terms, name='terms'),

    path('', comviews.home, name='home'),
    path('login/', relviews.log_in, name='login'),
    path('logout/', relviews.log_out, name='logout'),

    path('p/<str:phone_number>/', relviews.user_detail, name='user_detail'),
    path('r/<str:phone_number>/', relviews.user_reviews, name='user_reviews'),
    path('r/<str:phone_number>/new', relviews.review_create, name='review_create'),
    path('w/<str:phone_number>/', relviews.user_whatsapp, name='user_whatsapp'),

    path('users/', include('relationships.urls')),
    path('register/', include('relationships.urls_register')),
    path('login/', include('relationships.urls_login')),
        






    
    path('claim', relviews.claim, name='claim'),
    # path('register', relviews.register, name='register'),
    # path('register1', relviews.register1, name='register1'),
    path('verify-email', relviews.verify_email, name='verify_email'),

    path('enter-email', relviews.enter_email, name='enter_email'),

    # path('enter-status', relviews.enter_status, name='enter_status'),

    path('enter-phone-number', relviews.enter_number, name='enter_phone_number'),

    path('following', relviews.following, name='following'),



    path('review_detail', relviews.review_detail, name='review_detail'),

    path('contact_detail', relviews.contact_detail, name='contact_detail'),
    path('contact_reports', relviews.contact_reports, name='contact_reports'),
    path('report_create', relviews.report_create, name='report_create'),
    path('report_detail', relviews.report_detail, name='report_detail'),
    

    

    path('lookup', relviews.lookup, name='lookup'),
    

    # path('select-country', relviews.select_country, name='select-country'),
    # User menu and settings
    # path('credits', relviews.credits, name='credits'),
    # path('update-phone-number', relviews.update_phone_number, name='update_phone_number'),
    # path('update-requirements', relviews.requirements, name='update_requirements'),
    # path('link_email', relviews.link_email, name='link_email'),
    # Navigation bar
    # path('home', comviews.home, name='home'), # AKA search CHANGE
    # path('', relviews.user_list, name='search'), # AKA search CHANGE TO SEARCH
    # path('history', relviews.history, name='history'),
    # path('report', relviews.report, name='report'),
    # path('claim', relviews.claim, name='claim'),
    # path('faq', comviews.faq, name='faq'),
    # path('pricing', comviews.pricing, name='pricing'),
    # path('earn-money', comviews.earn_money, name='earn_money'),
    # path('claim_number', relviews.claim_number, name='claim_number'),
    # path('report_files', relviews.report_files, name='report_files'),

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