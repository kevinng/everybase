from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'leads'
urlpatterns = [
    # path('/', views.LeadListView.as_view(), name='list'), # get params for filter options, get option for this user's leads
    # path('<str:id>/', views.LeadDetailView.as_view(), name='detail'),
    # path('create/', views.LeadCreateView.as_view(), name='create'), # get to show form, post to create
    # path('<str:id>/update/', views.LeadUpdateView.as_view(), name='update'), # use new lead page as an example
    # path('<str:id>/contact/', views.contact_lead_owner, name='contact_lead_owner'), # contact lead owner
    # path('<str:id>/save/', views.save_lead, name='save_lead'), # save/unsave lead
    # path('saved/', views.SavedLeadListView, name='saved_leads'), # saved leads
    # path('documents/<str:id>', views.redirect_document, name='redirect_document'), # redirect to document
    # path('images/<str:id>', views.redirect_image, name='redirect_image'), # redirect to image
    # path('requests/accepted', views.AcceptedRequestListView.as_view(), name='accepted_requests'),
    # path('requests/pending', views.PendingRequestListView.as_view(), name='pending_requests'),







    # path(f'{webhook_root}/message/', views.TwilioIncomingMessageView.as_view()),
    # path(f'{webhook_root}/status/<str:msg_id>',
    #     views.TwilioIncomingStatusView.as_view(),
    #     name='status_update_message'),
    # path(f'{webhook_root}/status/',
    #     views.TwilioIncomingStatusView.as_view(), name='status_update'),
    # # path(f'{webhook_root}/fulfill/',
    # #     views.StripeFulfilmentCallbackView.as_view()),
    # # path(f'send_confirm_interests/', views.SendConfirmInterestsView.as_view())
]