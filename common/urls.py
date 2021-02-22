from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('country/',
        views.CountryList.as_view()),
    path('country/<int:pk>/',
        views.CountryDetail.as_view()),

    path('state/',
        views.StateList.as_view()),
    path('state/<int:pk>/',
        views.StateDetail.as_view()),

    path('import_job/',
        views.ImportJobList.as_view()),
    path('import_job/<int:pk>/',
        views.ImportJobDetail.as_view()),

    path('e/<str:file_to_render>', views.e),
]
urlpatterns = format_suffix_patterns(urlpatterns)