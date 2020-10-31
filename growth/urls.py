from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (GmassCampaignResultList, GmassCampaignResultDetail,
    GmassCampaignList, GmassCampaignDetail,
    ChemicalClusterOfSingaporeResultList,
    ChemicalClusterOfSingaporeResultDetail, Fibre2FashionResultList,
    Fibre2FashionResultDetail, ZeroBounceResultList, ZeroBounceResultDetail,
    DataSourceList, DataSourceDetail, SourcedEmailList, SourcedEmailDetail,
    ChemicalBookResultList, ChemicalBookResultDetail, LookChemResultList,
    LookChemResultDetail, WorldOfChemicalResultList,
    WorldOfChemicalResultDetail)

urlpatterns = [
    path('gmass_campaign_result/', GmassCampaignResultList.as_view()),
    path('gmass_campaign_result/<int:pk>/',
        GmassCampaignResultDetail.as_view()),
    path('gmass_campaign/', GmassCampaignList.as_view()),
    path('gmass_campaign/<int:pk>/', GmassCampaignDetail.as_view()),
    path('chemical_cluster_of_singapore_result/',
        ChemicalClusterOfSingaporeResultList.as_view()),
    path('chemical_cluster_of_singapore_result/<int:pk>/',
        ChemicalClusterOfSingaporeResultDetail.as_view()),
    path('fibre_2_fashion_result/', Fibre2FashionResultList.as_view()),
    path('fibre_2_fashion_result/<int:pk>/',
        Fibre2FashionResultDetail.as_view()),
    path('zero_bounce_result/', ZeroBounceResultList.as_view()),
    path('zero_bounce_result/<int:pk>/', ZeroBounceResultDetail.as_view()),
    path('data_source/', DataSourceList.as_view()),
    path('data_source/<int:pk>/', DataSourceDetail.as_view()),
    path('sourced_email/', SourcedEmailList.as_view()),
    path('sourced_email/<int:pk>/', SourcedEmailDetail.as_view()),
    path('chemical_book_result/', ChemicalBookResultList.as_view()),
    path('chemical_book_result/<int:pk>/', ChemicalBookResultDetail.as_view()),
    path('look_chem_result/', LookChemResultList.as_view()),
    path('look_chem_result/<int:pk>/', LookChemResultDetail.as_view()),
    path('world_of_chemicals_result/', WorldOfChemicalResultList.as_view()),
    path('world_of_chemicals_result/<int:pk>/',
        WorldOfChemicalResultDetail.as_view())
]
urlpatterns = format_suffix_patterns(urlpatterns)