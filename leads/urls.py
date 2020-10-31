from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [

    path('incoterm/',
        views.IncotermList.as_view()),
    path('incoterm/<int:pk>/',
        views.IncotermDetail.as_view()),

    path('currency/',
        views.CurrencyList.as_view()),
    path('currency/<int:pk>/',
        views.CurrencyDetail.as_view()),
    
    path('payment_mode/', 
        views.PaymentModeList.as_view()),
    path('payment_mode/<int:pk>/',
        views.PaymentModeDetail.as_view()),

    path('contact_type/',
        views.ContactTypeList.as_view()),
    path('contact_type/<int:pk>/',
        views.ContactTypeDetail.as_view()),

    path('lead_category/',
        views.LeadCategoryList.as_view()),
    path('lead_category/<int:pk>/',
        views.LeadCategoryDetail.as_view()),

    path('match_method/',
        views.MatchMethodList.as_view()),
    path('match_method/<int:pk>/',
        views.MatchMethodDetail.as_view()),

    path('match_status/',
        views.MatchStatusList.as_view()),
    path('match_status/<int:pk>/',
        views.MatchStatusDetail.as_view()),

    path('supply_quote_status/',
        views.SupplyQuoteStatusList.as_view()),
    path('supply_quote_status/<int:pk>/',
        views.SupplyQuoteStatusDetail.as_view()),

    path('demand_quote_status/',
        views.DemandQuoteStatusList.as_view()),
    path('demand_quote_status/<int:pk>/',
        views.DemandQuoteStatusDetail.as_view()),

    path('unit_of_measure/',
        views.UnitOfMeasureList.as_view()),
    path('unit_of_measure/<int:pk>/',
        views.UnitOfMeasureDetail.as_view()),

    path('uom_relationship/',
        views.UOMRelationshipList.as_view()),
    path('uom_relationship/<int:pk>/',
        views.UOMRelationshipDetail.as_view()),

    path('supply/',
        views.SupplyList.as_view()),
    path('supply/<int:pk>/',
        views.SupplyDetail.as_view()),

    path('demand/',
        views.DemandList.as_view()),
    path('demand/<int:pk>/',
        views.DemandDetail.as_view()),

    path('supply_quote/',
        views.SupplyQuoteList.as_view()),
    path('supply_quote/<int:pk>/',
        views.SupplyQuoteDetail.as_view()),

    path('production_capability/',
        views.ProductionCapabilityList.as_view()),
    path('production_capability/<int:pk>/',
        views.ProductionCapabilityDetail.as_view()),

    path('demand_quote/',
        views.DemandQuoteList.as_view()),
    path('demand_quote/<int:pk>/',
        views.DemandQuoteDetail.as_view()),

    path('trench/',
        views.TrenchList.as_view()),
    path('trench/<int:pk>/',
        views.TrenchDetail.as_view()),

    path('match/',
        views.MatchList.as_view()),
    path('match/<int:pk>/',
        views.MatchDetail.as_view()),

    path('supply_commission/',
        views.SupplyCommissionList.as_view()),
    path('supply_commission/<int:pk>/',
        views.SupplyCommissionDetail.as_view()),

    path('demand_commission/',
        views.DemandCommissionList.as_view()),
    path('demand_commission/<int:pk>/',
        views.DemandCommissionDetail.as_view())
]
urlpatterns = format_suffix_patterns(urlpatterns)