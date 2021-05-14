from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

webhook_root = 'webhooks/'
urlpatterns = [
    path(f'{webhook_root}messages/', views.TwilioIncomingMessageView.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)