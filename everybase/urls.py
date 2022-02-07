from relationships import views as relviews
from leads import views as leviews
from chat import views as chatviews

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
    # Common
    path('', leviews.AgentListView.as_view(), name='home'),

    # Leads
    path('leads/', include('leads.urls')),
    path('', leviews.AgentListView.as_view(), name='agents'),

    # Relationships
    path('register/', relviews.register, name='register'),
    path('confirm_register/<str:user_uuid>', relviews.confirm_register,
        name='confirm_register'),
    path('is_registered/<str:user_uuid>', relviews.is_registered,
        name='is_registered'),
    path('login/', relviews.log_in, name='login'),
    path('confirm_login/<str:user_uuid>', relviews.confirm_login,
        name='confirm_login'),
    path('is_logged_in/<str:user_uuid>', relviews.is_logged_in,
        name='is_logged_in'),
    path('logout/', relviews.log_out, name='logout'),
    path('users/', include('relationships.urls')),

    # Chat
    path('chat/', include('chat.urls')),

    # Files
    path('files/', include('files.urls')),

    # Django admin obfuscated URL
    path('3yJmUVGVJosFPDiZ6LyU4WARUiWXgMxCyfA6/', admin.site.urls),

    # Django Rest Framework login
    path('api-auth/', include('rest_framework.urls')),

    # Sentry debug URLs
    path('sentry-debug/', trigger_error), # trigger error
    path('sentry-debug-handled/', trigger_handled_error), # handle error

    # Common
    path('common/', include('common.urls')),
]

admin.site.site_header = "Everybase Admin"
admin.site.site_title = "" # No title
admin.site.index_title = "Welcome to Everybase Admin Portal"