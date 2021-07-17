from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'chat'
webhook_root = 'webhooks'
urlpatterns = [
    path(f'{webhook_root}/message/', views.TwilioIncomingMessageView.as_view()),
    path(f'{webhook_root}/status/<str:out_msg_id>',
        views.TwilioIncomingStatusView.as_view()),
    path(f'{webhook_root}/fulfill/',
        views.StripeFulfilmentCallbackView.as_view()),
    path(f'send_confirm_interests/', views.SendConfirmInterestsView.as_view())
]