from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (IncotermList, IncotermDetail, CurrencyList, CurrencyDetail,
    PaymentModeList, PaymentModeDetail, ContactTypeList, ContactTypeDetail,
    LeadCategoryList, LeadCategoryDetail, MatchMethodList, MatchMethodDetail,
    MatchStatusList, MatchStatusDetail, SupplyQuoteStatusList,
    SupplyQuoteStatusDetail, DemandQuoteStatusList, DemandQuoteStatusDetail)

urlpatterns = [
    path('incoterm/', IncotermList.as_view()),
    path('incoterm/<int:pk>/', IncotermDetail.as_view()),
    path('currency/', CurrencyList.as_view()),
    path('currency/<int:pk>/', CurrencyDetail.as_view()),
    path('payment_mode/', PaymentModeList.as_view()),
    path('payment_mode/<int:pk>/', PaymentModeDetail.as_view()),
    path('contact_type/', ContactTypeList.as_view()),
    path('contact_type/<int:pk>/', ContactTypeDetail.as_view()),
    path('lead_category/', LeadCategoryList.as_view()),
    path('lead_category/<int:pk>/', LeadCategoryDetail.as_view()),
    path('match_method/', MatchMethodList.as_view()),
    path('match_method/<int:pk>/', MatchMethodDetail.as_view()),
    path('match_status/', MatchStatusList.as_view()),
    path('match_status/<int:pk>/', MatchStatusDetail.as_view()),
    path('supply_quote_status/', SupplyQuoteStatusList.as_view()),
    path('supply_quote_status/<int:pk>/', SupplyQuoteStatusDetail.as_view()),
    path('demand_quote_status/', DemandQuoteStatusList.as_view()),
    path('demand_quote_status/<int:pk>/', DemandQuoteStatusDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)