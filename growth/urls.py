from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import GmassCampaignResultList, GmassCampaignResultDetail

url_patterns = [
    path('gmass_campaign_results/', GmassCampaignResultList.as_view()),
    path('gmass_campaign_results/<int:pk>/',
        GmassCampaignResultDetail.as_view()),
]
url_patterns = format_suffix_patterns(url_patterns)