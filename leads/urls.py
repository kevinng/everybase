from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (IncotermList, IncotermDetail, CurrencyList, CurrencyDetail)

urlpatterns = [
    path('incoterm/', IncotermList.as_view()),
    path('incoterm/<int:pk>/', IncotermDetail.as_view()),
    path('currency/', CurrencyList.as_view()),
    path('currency/<int:pk>/', CurrencyDetail.as_view())
]
urlpatterns = format_suffix_patterns(urlpatterns)