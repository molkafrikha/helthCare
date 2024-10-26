from django.db.models import Q, Exists, OuterRef, Subquery
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, permissions, status
from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from ...models.submisson import Event, EventPatient 
from ...models.Users import Patient, User
from mobicrowd.serializers.submissionSerializers import EventWorkerSerializer, EventSerializer

class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class UpcomingEventsListAPIView(generics.ListAPIView):
    queryset = Event.objects.filter(deadline__gt=timezone.now())
    serializer_class = EventSerializer

class PastEventsListAPIView(generics.ListAPIView):
    queryset = Event.objects.filter(deadline__lt=timezone.now())
    serializer_class = EventSerializer

class EventCreateView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventRetrieveView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventUpdateView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class UserInfoAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
        })

class EventDeleteView(generics.DestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class JoinEventView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, event_id):
        device_specs = request.data.get('device_specs', {})

        try:
            event = Event.objects.get(id=event_id)
            patient = request.user.patient_profile

            event_worker, created = EventPatient.objects.get_or_create(patient=patient, event=event)

            if not created:
                if event_worker.status == 'PENDING':
                    return Response({'message': 'Your request is pending', 'status': 'pending'})
                elif event_worker.status == 'APPROVED':
                    return Response({'message': 'You have already joined this event', 'status': 'approved'})

            event_worker.device_specs = device_specs
            event_worker.status = 'PENDING'
            event_worker.save()

            return Response({'message': 'Awaiting admin approval', 'status': 'waiting_approval'})
        except Event.DoesNotExist:
            return Response({'error': 'The event does not exist.'}, status=404)

class DeleteWorkerJoinView(APIView):
    def delete(self, request, event_worker_id):
        try:
            worker_join = EventPatient.objects.get(id=event_worker_id)
            worker_join.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except EventPatient.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class ApproveJoinRequestView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, event_worker_id):
        try:
            event_worker = EventPatient.objects.get(id=event_worker_id)

            if request.user.role == "Admin":
                event_worker.status = EventPatient.APPROVED
                event_worker.save()
                return Response({'message': 'Join request approved and patient added to event.'})
            else:
                return Response({'error': 'You are not authorized to approve this join request.'}, status=403)
        except EventPatient.DoesNotExist:
            return Response({'error': 'Join request does not exist.'}, status=404)

class PendingInvitationsView(generics.ListAPIView):
    serializer_class = EventWorkerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        if user.role == "Admin":
            return EventPatient.objects.filter(
                status=EventPatient.PENDING
            ).select_related('patient', 'event')
        else:
            return EventPatient.objects.none()

class RejectJoinRequestView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, event_worker_id):
        try:
            event_worker = EventPatient.objects.get(id=event_worker_id)

            if request.user.role == "Admin":
                event_worker.status = EventPatient.REJECTED
                event_worker.save()
                return Response({'message': 'Join request rejected.'})
            else:
                return Response({'error': 'You are not authorized to reject this join request.'}, status=403)
        except EventPatient.DoesNotExist:
            return Response({'error': 'Join request does not exist.'}, status=404)

class WorkerJoinedEventsByIdView(APIView):
    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, pk=patient_id)
        event_workers = EventPatient.objects.filter(patient=patient, status=EventPatient.APPROVED)
        joined_events = [ew.event for ew in event_workers]
        serializer = EventSerializer(joined_events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AvailableEventsForPatientView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not hasattr(user, 'patient_profile'):
            return Response({'error': 'User is not a patient.'}, status=status.HTTP_400_BAD_REQUEST)

        patient = user.patient_profile
        now = timezone.now()

        joined_event_ids = EventPatient.objects.filter(patient=patient).values_list('event_id', flat=True)
        pending_event_ids = EventPatient.objects.filter(patient=patient, status=EventPatient.PENDING).values_list('event_id', flat=True)

        available_events = Event.objects.filter(
            Q(id__in=pending_event_ids) |
            ~Q(id__in=joined_event_ids)
        ).filter(deadline__gt=now)

        serializer = EventSerializer(available_events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class WorkerJoinedEventsUpcomingView(APIView):
    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, pk=patient_id)
        event_workers = EventPatient.objects.filter(patient=patient, event__deadline__gt=timezone.now())
        upcoming_events = [ew.event for ew in event_workers]
        serializer = EventSerializer(upcoming_events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class WorkerEventStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id):
        user = request.user
        if not hasattr(user, 'patient_profile'):
            return Response({'error': 'User is not a patient.'}, status=status.HTTP_400_BAD_REQUEST)

        patient = user.patient_profile
        event = get_object_or_404(Event, pk=event_id)

        try:
            event_patient = EventPatient.objects.get(patient=patient, event=event, status='APPROVED')
            return Response({'status': 'APPROVED', 'message': 'Patient has joined the event with approved status.'})
        except EventPatient.DoesNotExist:
            return Response({'status': 'NOT APPROVED', 'message': 'Patient has not joined the event with approved status.'})

class WorkerJoinedEventsPastView(APIView):
    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, pk=patient_id)
        event_workers = EventPatient.objects.filter(patient=patient, event__deadline__lt=timezone.now())
        past_events = [ew.event for ew in event_workers]
        serializer = EventSerializer(past_events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EventRetrieveByIdView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer 

class EventRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(patient=self.request.user.patient_profile)

class PatientEventsAllView(generics.ListAPIView):
    serializer_class = EventSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        patient = self.request.user.patient_profile
        return Event.objects.filter(patient=patient)

class PatientEventsUpcomingView(generics.ListAPIView):
    serializer_class = EventSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        patient = self.request.user.patient_profile
        return Event.objects.filter(patient=patient, deadline__gt=timezone.now())

class PatientEventsPastView(generics.ListAPIView):
    serializer_class = EventSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        patient = self.request.user.patient_profile
        return Event.objects.filter(patient=patient, deadline__lt=timezone.now())

class EventFilter(filters.FilterSet):
    type = filters.CharFilter(field_name="type", lookup_expr='exact')
    patient = filters.CharFilter(field_name="patient__organization_name", lookup_expr='exact')
    cost = filters.RangeFilter(field_name="cost")
    numberOfPhotos = filters.RangeFilter(field_name="numberOfPhotos")
    deadline = filters.DateTimeFilter(field_name="deadline", lookup_expr='lte')
    startDate = filters.DateTimeFilter(field_name="startDate", lookup_expr='gte')

    class Meta:
        model = Event
        fields = ['type', 'patient', 'cost', 'numberOfPhotos', 'deadline', 'startDate']


class PendingPatientCountAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pending_patients_count = EventWorker.objects.filter(status='PENDING').count()
        return Response({'pending_patients_count': pending_patients_count})