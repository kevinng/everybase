from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (IncotermList, IncotermDetail, CurrencyList, CurrencyDetail,
    PaymentModeList, PaymentModeDetail, ContactTypeList, ContactTypeDetail,
    LeadCategoryList, LeadCategoryDetail, MatchMethodList, MatchMethodDetail,
    MatchStatusList, MatchStatusDetail, SupplyQuoteStatusList,
    SupplyQuoteStatusDetail, DemandQuoteStatusList, DemandQuoteStatusDetail,
    UnitOfMeasureList, UnitOfMeasureDetail, UOMRelationshipList,
    UOMRelationshipDetail, SupplyList, SupplyDetail, DemandList, DemandDetail,
    SupplyQuoteList, SupplyQuoteDetail, ProductionCapabilityList,
    ProductionCapabilityDetail, DemandQuoteList, DemandQuoteDetail, TrenchList,
    TrenchDetail, MatchList, MatchDetail)

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
    path('unit_of_measure/', UnitOfMeasureList.as_view()),
    path('unit_of_measure/<int:pk>/', UnitOfMeasureDetail.as_view()),
    path('uom_relationship/', UOMRelationshipList.as_view()),
    path('uom_relationship/<int:pk>/', UOMRelationshipDetail.as_view()),
    path('supply/', SupplyList.as_view()),
    path('supply/<int:pk>/', SupplyDetail.as_view()),
    path('demand/', DemandList.as_view()),
    path('demand/<int:pk>/', DemandDetail.as_view()),
    path('supply_quote/', SupplyQuoteList.as_view()),
    path('supply_quote/<int:pk>/', SupplyQuoteDetail.as_view()),
    path('production_capability/', ProductionCapabilityList.as_view()),
    path('production_capability/<int:pk>/',
        ProductionCapabilityDetail.as_view()),
    path('demand_quote/', DemandQuoteList.as_view()),
    path('demand_quote/<int:pk>/', DemandQuoteDetail.as_view()),
    path('trench/', TrenchList.as_view()),
    path('trench/<int:pk>/', TrenchDetail.as_view()),
    path('match/', MatchList.as_view()),
    path('match/<int:pk>/', MatchDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)