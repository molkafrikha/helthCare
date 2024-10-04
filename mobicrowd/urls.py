from django.urls import path
from mobicrowd.authentication.login import LoginView
from mobicrowd.authentication.registrationViews import  ApprovedRequestersListAPIView, LogoutAPIView, \
    ConfirmEmailAPIView, RequesterApprovalAPIView, \
    RequesterRejectionAPIView, ChangePasswordAPIView, ForgetPasswordView, PasswordResetConfirmView, \
    ActiveWorkersListAPIView, ApprovedRequestersListcountAPIView
from mobicrowd.authentication.user_registration import RegisterDoctorAPIView, RegisterPatientAPIView

    
from mobicrowd.views.apis.embeddingView import receive_embedding
from mobicrowd.views.apis.insert_scraped_data import upload_devices_file, DeviceListView
from mobicrowd.views.apis.users import UserRetrieveAPIView, ListPendingRequestersView

urlpatterns = [
    path('users/<int:id>', UserRetrieveAPIView.as_view(), name='user-detail'),
    
    path('register_doctor', RegisterDoctorAPIView.as_view(), name='register_doctor'),
    path('register_worker', RegisterPatientAPIView.as_view(), name='register_patient'),
    
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
    
    
    
    
    # decoder model api
    path('embedding/' , receive_embedding , name='receive_embedding' ),
    ##### events apis #############
   
]



