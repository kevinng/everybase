from django.urls import path
from . import views

app_name = 'leads__root'
urlpatterns = [
    path('', views.AgentListView.as_view(), name='agents'),
    path('i-need-agents', views.INeedAgentListView.as_view(), name='i_need_agents'),
    path('i-need-agents/new', views.create_i_need_agent, name='create_i_need_agent'),
    path('i-need-agents/<int:pk>', views.i_need_agent_detail, name='i_need_agent_detail')
]