from django.contrib.auth import get_user_model, authenticate
from django.core.mail import EmailMessage, send_mail
from django.db import transaction
from django.template.loader import render_to_string
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from Mobicrowd_backend_project import settings
from mobicrowd.authentication.email_sending import send_verification_email
from mobicrowd.models.Users import User, Token, Doctor, Patient


class ConfirmEmailAPIView(APIView):
    def get(self, request, pk, token):
        try:
            user = User.objects.get(pk=pk)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'message': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        token_obj = Token.objects.filter(user=user).first()
        if user is not None and token_obj:
            token_generator = PasswordResetTokenGenerator()
            if token_generator.check_token(user, token) and token_obj.token == token:
                user.is_active = True
                user.save()
                token_obj.delete()
                signin_url = f'{settings.frontendUrl}/authentication'
                return Response({'message': 'Your account has been confirmed. Thank you!', 'redirect_url': signin_url},
                                status=status.HTTP_200_OK)

        return Response({'message': 'The confirmation link is invalid or has expired.'},
                        status=status.HTTP_400_BAD_REQUEST)


class RequesterApprovalAPIView(APIView):
    # permission_classes = [IsAuthenticated,]
    def post(self, request, email):
        print(request.user)
        Doctor = get_object_or_404(Doctor, user__email=email)
        print(Doctor.approved)
        Doctor.approved = True
        user = Doctor.user
        user.save()
        Doctor.save()
        print(Doctor.approved)

        send_verification_email(user)
        return Response({'success': 'Customer account approved successfully.'}, status=status.HTTP_200_OK)


class ActiveWorkersListAPIView(APIView):
    def get(self, request):
        # Filter users who are active and are patient
        active_users = User.objects.filter(is_active=True, is_patient=True)

        # Fetch related patient data
        patients = patient.objects.filter(user__in=active_users)

        # Prepare the data to be returned
        data = [
            {
                'id': Patient.user.id,
                'fullName': Patient.user.fullName,
                'email': Patient.user.email,
                'location': Patient.location,
                
                'mobile_phone': Patient.user.mobile_phone,
                # Include other fields as needed
            }
            for Patient in patients
        ]

        return Response(data, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        # Déconnexion de l'utilisateur
        logout(request)
        return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)


class RequesterRejectionAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def delete(self, request, email):
        Doctor = get_object_or_404(Doctor, user__email=email)
        Doctor.user.delete()
        return Response({'success': 'Doctor account rejected and deleted successfully.'}, status=status.HTTP_200_OK)


class ApprovedRequestersListAPIView(APIView):
    def get(self, request):
        approved_requesters = Doctor.objects.filter(approved=True).select_related('user')
        data = [
            {

                'fullName': Doctor.user.fullName,
                'email': Doctor.user.email,
                
                'location': Doctor.location,
                'mobile_phone': Doctor.user.mobile_phone,
            }
            for Doctor in approved_requesters
        ]
        return Response(data, status=status.HTTP_200_OK)


class ApprovedRequestersListcountAPIView(APIView):
    def get(self, request):
        count = Doctor.objects.filter(approved=0).count()  # Assuming approved is a boolean field
        return JsonResponse({'not_approved_count': count})


class ChangePasswordAPIView(APIView):
    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user's email and password are correct

        # Change the user's password
        new_password = request.data.get('password', None)
        if not new_password:
            return Response({'error': 'New password is required.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)


class CustomPasswordResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(user.password) + str(timestamp)


def send_forget_password_email(user, reset_password_link):
    subject = 'BrightSkies academy account credentials'
    context = {
        'full_name': user.fullName,
        'email': user.email,
        'reset_password_link': reset_password_link,
    }
    body = render_to_string('forget_password', context)
    email = EmailMessage(subject=subject, body=body, from_email=settings.EMAIL_HOST_USER, to=[user.email])
    email.content_subtype = 'html'
    email.send()


def password_forgotten_reset(user):
    token_generator = CustomPasswordResetTokenGenerator()
    token = token_generator.make_token(user)

    # Check if a token already exists for the user
    existing_token = Token.objects.filter(user=user).first()

    if existing_token:
        # Update the existing token
        existing_token.token = token
        existing_token.save()
    else:
        # Create a new token if none exists
        Token.objects.create(user=user, token=token)

    reset_password_link = f'http://localhost:4200/authentication/set-new-password/{user.pk}/{token}'
    send_forget_password_email(user, reset_password_link)
    return Response({'message': 'Email sent'}, status=status.HTTP_200_OK)


class ForgetPasswordView(APIView):
    def get(self, request, email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response('This email address does not exist')

        password_forgotten_reset(user)
        return Response({'message': 'Email sent'}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    def get(self, request, user_id, token):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        token_obj = Token.objects.filter(user=user).first()
        if not token_obj:
            return Response({'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        token_generator = CustomPasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            return Response({'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        # Redirect to the reset password page with the token and user id as query parameters
        reset_password_url = f'{settings.frontendUrl}/authentication/reset-password?token={token}&user_id={user.pk}'
        return redirect(reset_password_url)

    def post(self, request, user_id, token):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        token_obj = Token.objects.filter(user=user).first()
        if not token_obj:
            return Response({'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        token_generator = CustomPasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            return Response({'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if password != confirm_password:
            return Response('Passwords do not match')

        user.set_password(password)
        user.save()

        token_obj.delete()

        return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)