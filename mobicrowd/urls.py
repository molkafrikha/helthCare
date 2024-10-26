from django.urls import path, include
from mobicrowd.authentication.login import LoginView
from mobicrowd.authentication.registrationViews import ( 
    ApprovedRequestersListAPIView, LogoutAPIView, ConfirmEmailAPIView, 
    RequesterApprovalAPIView, RequesterRejectionAPIView, 
    ChangePasswordAPIView, ForgetPasswordView, PasswordResetConfirmView, 
    ActiveWorkersListAPIView, ApprovedRequestersListcountAPIView
)
from mobicrowd.authentication.user_registration import RegisterDoctorAPIView, RegisterPatientAPIView
from mobicrowd.views.apis.embeddingView import receive_embedding
from mobicrowd.views.apis.insert_scraped_data import upload_devices_file, DeviceListView
from mobicrowd.views.apis.users import UserRetrieveAPIView, ListPendingRequestersView

# Import your Assessment and AssessmentResult views
from mobicrowd.views.apis.assessments import AssessmentViewSet, AssessmentResultViewSet
from rest_framework.routers import DefaultRouter

# Create a router and register your assessment viewsets
router = DefaultRouter()
router.register(r'assessments', AssessmentViewSet, basename='assessments')
router.register(r'assessment-results', AssessmentResultViewSet, basename='assessment-results')

urlpatterns = [
    path('users/<int:id>/', UserRetrieveAPIView.as_view(), name='user-detail'),
    path('register-doctor/', RegisterDoctorAPIView.as_view(), name='register_doctor'),
    path('register-worker/', RegisterPatientAPIView.as_view(), name='register_patient'),
    path('login/', LoginView.as_view(), name='login'),
    path('account-confirm-email/<int:pk>/<str:token>/', ConfirmEmailAPIView.as_view(), name='account_confirm_email'),
    path('requester/<str:email>/approve-account/', RequesterApprovalAPIView.as_view(), name='approve-requester-account'),
    path('requester/<str:email>/reject-account/', RequesterRejectionAPIView.as_view(), name='reject-requester-account'),
    path('requesters/approved/', ApprovedRequestersListAPIView.as_view(), name='approved-requesters-list'),
    path('user/<int:user_id>/change-password/', ChangePasswordAPIView.as_view(), name='change-password'),
    path('forget-password/<str:email>/', ForgetPasswordView.as_view(), name='forget_password'),
    path('set-new-password/<int:user_id>/<str:token>/', PasswordResetConfirmView.as_view(), name='set-new-password'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('pending-requesters/', ListPendingRequestersView.as_view(), name='list_pending_requesters'),

    # decoder model api
    path('embedding/', receive_embedding, name='receive_embedding'),

    # Include the router URLs for assessments
    path('', include(router.urls)),  # Add this line to include the assessment URLs
]
