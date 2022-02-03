from django.urls import path
from . import views

app_name = 'leads__root'
urlpatterns = [
    path('', views.AgentListView.as_view(), name='agents'),
    path('leads', views.LeadListView.as_view(), name='lead_list'),
    path('leads/create', views.lead_create, name='lead_create'),
    path('leads/edit/<int:pk>', views.LeadEdit.as_view(), name='lead_edit'),
    path('leads/<int:pk>', views.LeadDetail.as_view(), name='lead_detail'),

    # path('u/<int:pk>/i-need-agents')


    # path('i-need-agents/author/<int:user_pk>')
]