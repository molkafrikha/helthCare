from django.urls import path
from mobicrowd.authentication.login import LoginView
from mobicrowd.authentication.registrationViews import  ApprovedRequestersListAPIView, LogoutAPIView, \
    ConfirmEmailAPIView, RequesterApprovalAPIView, \
    RequesterRejectionAPIView, ChangePasswordAPIView, ForgetPasswordView, PasswordResetConfirmView, \
    ActiveWorkersListAPIView, ApprovedRequestersListcountAPIView
from mobicrowd.authentication.user_registration import RegisterDoctorAPIView, RegisterPatientAPIView
from mobicrowd.views.apis.sentimentAnalysis import   CommentCreateView  ,EventCommentsView
from mobicrowd.views.apis.embeddingView import receive_embedding
from mobicrowd.views.apis.insert_scraped_data import upload_devices_file, DeviceListView
from mobicrowd.views.apis.users import UserRetrieveAPIView, ListPendingRequestersView
from mobicrowd.views.apis.event_views import DeleteWorkerJoinView, AvailableEventsForPatientView ,\
     RejectJoinRequestView, \
    PendingInvitationsView, EventRetrieveByIdView, JoinEventView, \
    EventListView, EventRetrieveView, EventCreateView, EventUpdateView, EventDeleteView, ApproveJoinRequestView, \
    UserInfoAPIView, UpcomingEventsListAPIView, PastEventsListAPIView,  \
    WorkerJoinedEventsUpcomingView, WorkerJoinedEventsPastView, WorkerJoinedEventsByIdView, PatientEventsPastView, \
    PatientEventsAllView, PatientEventsUpcomingView, PendingPatientCountAPIView, WorkerEventStatusView 


urlpatterns = [
    path('users/<int:id>', UserRetrieveAPIView.as_view(), name='user-detail'),
    
    path('register_doctor', RegisterDoctorAPIView.as_view(), name='register_doctor'),
    path('registe_patient', RegisterPatientAPIView.as_view(), name='register_patient'),
    
    path('login', LoginView.as_view(), name='login'),
    path('account_confirm_email/<int:pk>/<str:token>', ConfirmEmailAPIView.as_view(), name='account_confirm_email'),
    path('requester/<str:email>/approve-account', RequesterApprovalAPIView.as_view(), name='approve-requester-account'),
    path('requester/<str:email>/reject-account', RequesterRejectionAPIView.as_view(), name='reject-requester-account'),
    path('requesters/approved', ApprovedRequestersListAPIView.as_view(), name='approved-requesters-list'),
    path('user/<int:user_id>/change-password', ChangePasswordAPIView.as_view(), name='change-password'),
    path('forget-password/<str:email>', ForgetPasswordView.as_view(), name='forget_password'),
    path('set-new-password/<int:user_id>/<str:token>', PasswordResetConfirmView.as_view(), name='set-new-password'),
    path('logout', LogoutAPIView.as_view(), name='logout'),

     
    path('PendingRequester', ListPendingRequestersView.as_view(), name='listpendingRequester'),
    
    
    # event api 
    path('events/<int:pk>', EventRetrieveByIdView.as_view(), name='event-retrieve-by-id'),
    path('events/requester/all', PatientEventsAllView.as_view(), name='requester-events'),
    path('events/requester/upcoming', PatientEventsUpcomingView.as_view(), name='requester-events'),
    path('events/requester/past', PatientEventsPastView.as_view(), name='requester-events'),
    
    path('events', EventListView.as_view(), name='event-list'),
    path('events/create', EventCreateView.as_view(), name='event-create'),
    path('events/<int:pk>', EventRetrieveView.as_view(), name='event-detail'),
    path('events/<int:pk>/update', EventUpdateView.as_view(), name='event-update'),
    path('events/<int:pk>/delete', EventDeleteView.as_view(), name='event-delete'),
    path('events/join/<int:event_id>', JoinEventView.as_view(), name='join-event'),
    path('events/approve/<int:event_worker_id>', ApproveJoinRequestView.as_view(), name='approve-join-request'),
    path('events/refuse/<int:event_worker_id>', RejectJoinRequestView.as_view(), name='approve-join-request'),
    path('worker/<int:worker_id>/events/joined/all', WorkerJoinedEventsByIdView.as_view(), name='worker-joined-events'),
    path('worker/<int:worker_id>/events/joined/upcoming', WorkerJoinedEventsUpcomingView.as_view(), name='worker-joined-events'),
    path('worker/<int:worker_id>/events/joined/past', WorkerJoinedEventsPastView.as_view(), name='worker-joined-events'),
    path('events/past', PastEventsListAPIView.as_view(), name='past-events-list'),
    path('events/upcoming', UpcomingEventsListAPIView.as_view(), name='upcoming-events-list'),
    
     path('eventworker/delete/<int:event_worker_id>/', DeleteWorkerJoinView.as_view(), name='delete-worker-join'),
    path('active-workers', ActiveWorkersListAPIView.as_view(), name='active-workers-list'),
    path('requester-count', ApprovedRequestersListcountAPIView.as_view(), name='not-approved-requesters-count'),
    path('pending-workers-count', PendingPatientCountAPIView.as_view(), name='pending-workers-count'),
    path('events/available-for-worker', AvailableEventsForPatientView.as_view(), name='available-events-for-worker'),
    path('events/<int:event_id>/worker_status', WorkerEventStatusView.as_view(), name='worker_event_status'),
    path('pending-invitations', PendingInvitationsView.as_view(), name='pending-invitations'),
    path('events/<int:event_id>/comments', EventCommentsView.as_view(), name='event-comments'),  # URL pour récupérer les commentaires d'un événement
    # decoder model api
    path('comments', CommentCreateView.as_view(), name='comment-create'),
    
    ##### events apis #############
   
]



