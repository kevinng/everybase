from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('gmass_campaign_results/',
        views.GmassCampaignResultList.as_view()),
    path('gmass_campaign_results/<int:pk>/',
        views.GmassCampaignResultDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)