from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'leads__root'
urlpatterns = [
    path('', views.LeadListView.as_view(), name='list'), # get params for filter options, get option for this user's leads

    # path('documents/<str:id>', views.redirect_document, name='redirect_document'), # redirect to document
    # path('images/<str:id>', views.redirect_image, name='redirect_image'), # redirect to image
    # path('requests/accepted', views.AcceptedRequestListView.as_view(), name='accepted_requests'),
    # path('requests/pending', views.PendingRequestListView.as_view(), name='pending_requests'),
]