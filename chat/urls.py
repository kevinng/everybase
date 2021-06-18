from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'chat'
webhook_root = 'webhooks'
urlpatterns = [
    # Webhooks
    path(f'{webhook_root}/message_v1/',
        views.TwilioIncomingMessageView.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)