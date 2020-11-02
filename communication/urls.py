from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [

    path('issue/',
        views.IssueList.as_view()),
    path('issue/<int:pk>/',
        views.IssueDetail.as_view()),

    path('issue_tag/',
        views.IssueTagList.as_view()),
    path('issue_tag/<int:pk>/',
        views.IssueTagDetail.as_view()),

    path('issue_status/',
        views.IssueStatusList.as_view()),
    path('issue_status/<int:pk>/',
        views.IssueStatusDetail.as_view()),

    path('conversation/',
        views.ConversationList.as_view()),
    path('conversation/<int:pk>/',
        views.ConversationDetail.as_view()),

    path('conversation_channel/',
        views.ConversationChannelList.as_view()),
    path('conversation_channel/<int:pk>/',
        views.ConversationChannelDetail.as_view()),

    path('conversation_email/',
        views.ConversationEmailList.as_view()),
    path('conversation_email/<int:pk>/',
        views.ConversationEmailDetail.as_view()),

    path('conversation_email_status/',
        views.ConversationEmailStatusList.as_view()),
    path('conversation_email_status/<int:pk>/',
        views.ConversationEmailStatusDetail.as_view()),

    path('conversation_chat/',
        views.ConversationChatList.as_view()),
    path('conversation_chat/<int:pk>/',
        views.ConversationChatDetail.as_view()),

    path('conversation_chat_status/',
        views.ConversationChatStatusList.as_view()),
    path('conversation_chat_status/<int:pk>/',
        views.ConversationChatStatusDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)