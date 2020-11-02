from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [

    path('issue/',
        views.IssueList.as_view()),
    path('issue/<int:pk>/',
        views.IssueDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)