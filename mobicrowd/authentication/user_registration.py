from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mobicrowd.authentication.email_sending import send_verification_email
from mobicrowd.models.Users import User
from mobicrowd.serializers.usersSerializers import (
    DoctorSerializer, PatientSerializer, UserSerializer
)
from allauth.account.models import EmailAddress


def email_address_exists(email):
    return EmailAddress.objects.filter(email=email).exists()


class RegisterDoctorAPIView(APIView):

    def post(self, request):
        if email_address_exists(request.data.get('email')):
            return Response({'message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = DoctorSerializer(data={
                'user': {
                    'email': request.data.get('email'),
                    'password': request.data.get('password'),
                    'fullName': request.data.get('fullName'),
                    'mobile_phone': request.data.get('mobile_phone'),
                    'is_doctor': True,
                    'is_active': False,
                    'role': 'Doctor',
                },
                
                
                'address': request.data.get('address'),
            })

            if serializer.is_valid():
                doctor = serializer.save()
                user = doctor.user

                send_verification_email(user)

                return Response({'message': 'Verification email sent. Please verify your account.'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterPatientAPIView(APIView):

    def post(self, request):
        if email_address_exists(request.data.get('email')):
            return Response({'message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = PatientSerializer(data={
                'user': {
                    'email': request.data.get('email'),
                    'password': request.data.get('password'),
                    'fullName': request.data.get('fullName'),
                    'mobile_phone': request.data.get('mobile_phone'),
                    'is_patient': True,
                    'is_active': False,
                    'role': 'Patient',
                },
                'date_of_birth': request.data.get('date_of_birth'),
                'gender': request.data.get('gender'),
                'phone_number': request.data.get('phone_number'),
                'address': request.data.get('address'),
                'medical_history': request.data.get('medical_history'),
            })

            if serializer.is_valid():
                patient = serializer.save()
                user = patient.user

                send_verification_email(user)

                return Response({'message': 'Verification email sent. Please verify your account.'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
