from django.urls import path
from . import views

app_name = 'leads__root'
urlpatterns = [
    path('', views.AgentListView.as_view(), name='agents'),
    path('i-need-agents', views.INeedAgentListView.as_view(), name='i_need_agents'),
    # path('i-need-agents/author/<int:user_pk>')
    path('i-need-agent/new', views.create_i_need_agent, name='create_i_need_agent'),
    path('i-need-agent/<int:pk>', views.INeedAgentDetail.as_view(), name='i_need_agent_detail'),
]