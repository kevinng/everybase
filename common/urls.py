from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [

    path('country/',
        views.CountryList.as_view()),
    path('country/<int:pk>/',
        views.CountryDetail.as_view()),

    path('state/',
        views.StateList.as_view()),
    path('state/<int:pk>/',
        views.StateDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)