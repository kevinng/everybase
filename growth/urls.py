from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [

    path('gmass_campaign_result/',
        views.GmassCampaignResultList.as_view()),
    path('gmass_campaign_result/<int:pk>/',
        views.GmassCampaignResultDetail.as_view()),

    path('gmass_campaign/',
        views.GmassCampaignList.as_view()),
    path('gmass_campaign/<int:pk>/',
        views.GmassCampaignDetail.as_view()),

    path('chemical_cluster_of_singapore_result/',
        views.ChemicalClusterOfSingaporeResultList.as_view()),
    path('chemical_cluster_of_singapore_result/<int:pk>/',
        views.ChemicalClusterOfSingaporeResultDetail.as_view()),

    path('fibre2fashion_buying_offer/',
        views.Fibre2FashionBuyingOfferList.as_view()),
    path('fibre2fashion_buying_offer/<int:pk>/',
        views.Fibre2FashionBuyingOfferDetail.as_view()),

    path('fibre2fashion_selling_offer/',
        views.Fibre2FashionSellingOfferList.as_view()),
    path('fibre2fashion_selling_offer/<int:pk>/',
        views.Fibre2FashionSellingOfferDetail.as_view()),

    path('zero_bounce_result/',
        views.ZeroBounceResultList.as_view()),
    path('zero_bounce_result/<int:pk>/',
        views.ZeroBounceResultDetail.as_view()),

    path('data_source/',
        views.DataSourceList.as_view()),
    path('data_source/<int:pk>/',
        views.DataSourceDetail.as_view()),

    path('sourced_email/',
        views.SourcedEmailList.as_view()),
    path('sourced_email/<int:pk>/',
        views.SourcedEmailDetail.as_view()),

    path('chemical_book_supplier/',
        views.ChemicalBookSupplierList.as_view()),
    path('chemical_book_supplier/<int:pk>/',
        views.ChemicalBookSupplierDetail.as_view()),

    path('look_chem_supplier/',
        views.LookChemSupplierList.as_view()),
    path('look_chem_supplier/<int:pk>/',
        views.LookChemSupplierDetail.as_view()),

    path('world_of_chemicals_result/',
        views.WorldOfChemicalResultList.as_view()),
    path('world_of_chemicals_result/<int:pk>/',
        views.WorldOfChemicalResultDetail.as_view())
]
urlpatterns = format_suffix_patterns(urlpatterns)