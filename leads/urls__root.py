from django.urls import path
from . import views

app_name = 'leads__root'
urlpatterns = [
    path('', views.AgentListView.as_view(), name='agents')
]