from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'chat'
webhook_root = 'webhooks'
urlpatterns = [
    path(f'{webhook_root}/message/', views.TwilioIncomingMessageView.as_view()),
    path(f'{webhook_root}/status/', views.TwilioIncomingStatusView.as_view()),
    path(f'send_confirm_interests/', views.SendConfirmInterestsView.as_view())
]
urlpatterns = format_suffix_patterns(urlpatterns)