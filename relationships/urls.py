from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [

    path('person_link_type/',
        views.PersonLinkTypeList.as_view()),
    path('person_link_type/<int:pk>/',
        views.PersonLinkTypeDetail.as_view()),

    path('person_link/',
        views.PersonLinkList.as_view()),
    path('person_link/<int:pk>/',
        views.PersonLinkDetail.as_view()),

    path('person_company_type/',
        views.PersonCompanyTypeList.as_view()),
    path('person_company_type/<int:pk>/',
        views.PersonCompanyTypeDetail.as_view()),

    path('person_company/',
        views.PersonCompanyList.as_view()),
    path('person_company/<int:pk>/',
        views.PersonCompanyDetail.as_view()),
        
    path('person_address_type/',
        views.PersonAddressTypeList.as_view()),
    path('person_address_type/<int:pk>/',
        views.PersonAddressTypeDetail.as_view()),

    path('person_address/',
        views.PersonAddressList.as_view()),
    path('person_address/<int:pk>/',
        views.PersonAddressDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)