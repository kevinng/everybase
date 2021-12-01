from django.urls import path
from . import views

app_name = 'leads__root'
urlpatterns = [
    path('', views.LeadListView.as_view(), name='list'),
    path('contact_requests/<str:uuid>/', views.contact_request_detail,
        name='contact_request_detail'),
    path('contact_requests/', views.ContactRequestListView.as_view(),
        name='contact_request_list'),
]