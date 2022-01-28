from django.urls import path
from . import views

app_name = 'leads__root'
urlpatterns = [
    path('', views.AgentListView.as_view(), name='agents'),
    path('i-need-agents', views.i_need_agents, name='i_need_agents')
]