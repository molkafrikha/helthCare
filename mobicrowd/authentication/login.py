import datetime

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken

from mobicrowd.models.Users import User


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'id': user.id,
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'role': user.role  # Convert queryset to list

    }

class LoginView(APIView):
    def post(self, request):
        if 'email' not in request.data or 'password' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        
        email = request.data['email']
        password = request.data['password']
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            auth_data = get_tokens_for_user(request.user)
            return Response({'msg': 'Login Success', **auth_data}, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)