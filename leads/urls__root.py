from django.urls import path
from . import views

app_name = 'leads__root'
urlpatterns = [
    path('', views.LeadListView.as_view(), name='list'),
    path('messages/<str:uuid>/', views.message_detail, name='message_detail'),
    path('messages/', views.message_list, name='message_list'),
]