from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [

    path('person_link_type/',
        views.PersonLinkTypeList.as_view()),
    path('person_link_type/<int:pk>/',
        views.PersonLinkTypeDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)