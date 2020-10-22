from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (GmassCampaignResultList, GmassCampaignResultDetail,
    GmassCampaignList, GmassCampaignDetail)

urlpatterns = [
    path('gmass_campaign_result/', GmassCampaignResultList.as_view()),
    path('gmass_campaign_result/<int:pk>/',
        GmassCampaignResultDetail.as_view()),
    path('gmass_campaign/', GmassCampaignList.as_view()),
    path('gmass_campaign/<int:pk>/', GmassCampaignDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)