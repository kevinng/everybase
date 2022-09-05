from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    # path('sm/<str:file_to_render>', views.sm), # Render Superio mock-ups
    # path('ml/<str:file_to_render>', views.ml), # Render Metronic layout builder exports
    # path('mm/<str:file_to_render>', views.mm), # Render Metronic mock-ups

    # path('country/',
    #     views.CountryList.as_view()),
    # path('country/<int:pk>/',
    #     views.CountryDetail.as_view()),

    # path('state/',
    #     views.StateList.as_view()),
    # path('state/<int:pk>/',
    #     views.StateDetail.as_view()),

    # path('import_job/',
    #     views.ImportJobList.as_view()),
    # path('import_job/<int:pk>/',
    #     views.ImportJobDetail.as_view()),

    # path('e/<str:file_to_render>', views.e),
    # path('m/<str:file_to_render>', views.m),
]
urlpatterns = format_suffix_patterns(urlpatterns)