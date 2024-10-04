import re
from django.db.models import Q

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status

from mobicrowd.models.Users import User ,Doctor , Patient
from mobicrowd.serializers.usersSerializers import UserSerializer, DoctorSerializer ,PatientSerializer

from django_filters import rest_framework as filters


class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id' # Defines the name of the URL parameter



class ListPendingRequestersView(APIView):
    def get(self, request):
        Doctors = doctor.objects.filter( approved=False)
        serializer = DoctorSerializer(Doctors, many=True)
        return Response(serializer.data)





