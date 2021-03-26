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

    path('chemical_cluster_of_singapore_company/',
        views.ChemicalClusterOfSingaporeCompanyList.as_view()),
    path('chemical_cluster_of_singapore_company/<int:pk>/',
        views.ChemicalClusterOfSingaporeCompanyDetail.as_view()),

    path('chemical_cluster_of_singapore_product/',
        views.ChemicalClusterOfSingaporeProductList.as_view()),
    path('chemical_cluster_of_singapore_product/<int:pk>/',
        views.ChemicalClusterOfSingaporeProductDetail.as_view()),

    path('chemical_cluster_of_singapore_service/',
        views.ChemicalClusterOfSingaporeServiceList.as_view()),
    path('chemical_cluster_of_singapore_service/<int:pk>/',
        views.ChemicalClusterOfSingaporeServiceDetail.as_view()),

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
        
    path('chemical_book_supplier/',
        views.ChemicalBookSupplierList.as_view()),
    path('chemical_book_supplier/<int:pk>/',
        views.ChemicalBookSupplierDetail.as_view()),

    path('look_chem_supplier/',
        views.LookChemSupplierList.as_view()),
    path('look_chem_supplier/<int:pk>/',
        views.LookChemSupplierDetail.as_view()),

    path('world_of_chemicals_supplier/',
        views.WorldOfChemicalsSupplierList.as_view()),
    path('world_of_chemicals_supplier/<int:pk>/',
        views.WorldOfChemicalsSupplierDetail.as_view()),

    path('ok_chem_buying_request/',
        views.OKChemBuyingRequestList.as_view()),
    path('ok_chem_buying_request/<int:pk>/',
        views.OKChemBuyingRequestDetail.as_view())
]
urlpatterns = format_suffix_patterns(urlpatterns)