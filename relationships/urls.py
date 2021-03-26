from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('phone_number_type/',
        views.PhoneNumberTypeList.as_view()),
    path('phone_number_type/<int:pk>/',
        views.PhoneNumberTypeDetail.as_view()),

    path('phone_number/',
        views.PhoneNumberList.as_view()),
    path('phone_number/<int:pk>/',
        views.PhoneNumberDetail.as_view()),

    path('email/',
        views.EmailList.as_view()),
    path('email/<int:pk>/',
        views.EmailDetail.as_view()),

    path('invalid_email/',
        views.InvalidEmailList.as_view()),
    path('invalid_email/<int:pk>/',
        views.InvalidEmailDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)