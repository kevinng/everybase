from django.urls import path
from relationships import views

app_name = 'relationships'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('register_link/<str:user_uuid>', views.register_link,
        name='register_link'),
    path('cr/<str:user_uuid>', views.confirm_register, name='confirm_register'),
    path('login_link/<str:token_str>', views.log_in_link, name='login_link'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('cl/<str:token_str>', views.confirm_log_in, name='confirm_login'),
    # path('log_in_if_logged_in/<str:token_str>', views.log_in_if_logged_in,
    #     name='log_in_if_logged_in'),
    path('log_in_if_registered/<str:token_str>', views.log_in_if_registered,
        name='log_in_if_registered')
    
    # path('contacts/', views.ContactListView.as_view(), name='contacts'),



    # path('/', views.LeadListView.as_view(), name='list'), # get params for filter options, get option for this user's leads
    # path('<str:id>/', views.LeadDetailView.as_view(), name='detail'),
    # path('create/', views.LeadCreateView.as_view(), name='create'), # get to show form, post to create
    # path('<str:id>/update/', views.LeadUpdateView.as_view(), name='update'), # missing mockup
    # path('<str:id>/contact/', views.contact, name='contact'), # contact lead owner
    # path('<str:id>/save/', views.save, name='save'), # save/unsave lead
    # path('documents/<str:id>', views.LeadDocumentDetailView.as_view(), name='document_detail'), # redirect to document
    # path('images/<str:id>', views.LeadImageDetailView.as_view(), name='image_detail'), # redirect to image
    # path('requests/accepted', views.AcceptedRequestListView.as_view(), name='accepted_request_list'),
    # path('requests/pending', views.PendingRequestListView.as_view(), name='pending_request_list'),

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