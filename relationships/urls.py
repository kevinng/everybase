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

    path('person_phone_number_type/',
        views.PersonPhoneNumberTypeList.as_view()),
    path('person_phone_number_type/<int:pk>/',
        views.PersonPhoneNumberTypeDetail.as_view()),

    path('person_phone_number/',
        views.PersonPhoneNumberList.as_view()),
    path('person_phone_number/<int:pk>/',
        views.PersonPhoneNumberDetail.as_view()),

    path('person_email_type/',
        views.PersonEmailTypeList.as_view()),
    path('person_email_type/<int:pk>/',
        views.PersonEmailTypeDetail.as_view()),

    path('person_email/',
        views.PersonEmailTypeList.as_view()),
    path('person_email/<int:pk>/',
        views.PersonEmailTypeDetail.as_view()),

    path('company_link_type/',
        views.CompanyLinkTypeList.as_view()),
    path('company_link_type/<int:pk>/',
        views.CompanyLinkTypeDetail.as_view()),

    path('company_address_type/',
        views.CompanyAddressTypeList.as_view()),
    path('company_address_type/<int:pk>/',
        views.CompanyAddressTypeDetail.as_view()),

    path('company_address/',
        views.CompanyAddressList.as_view()),
    path('company_address/<int:pk>/',
        views.CompanyAddressDetail.as_view()),

    path('company_phone_number_type/',
        views.CompanyPhoneNumberTypeList.as_view()),
    path('company_phone_number_type/<int:pk>/',
        views.CompanyPhoneNumberTypeDetail.as_view()),

    path('company_phone_number/',
        views.CompanyPhoneNumberList.as_view()),
    path('company_phone_number/<int:pk>/',
        views.CompanyPhoneNumberDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)