from rest_framework import serializers
from mobicrowd.models.submisson import EventPatient, Event, Reward, PatientReward , Comment

class EventWorkerSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source='event.title')
    patient_id = serializers.CharField(source='patient.user.id')  # Utiliser `patient` à la place de `worker`

    class Meta:
        model = EventPatient
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    joined_patients = serializers.SerializerMethodField()  # Mettre à jour à `joined_patients`
    requester_organization_name = serializers.CharField(source='requester.organization_name', read_only=True)
    requester_location = serializers.CharField(source='requester.location', read_only=True)

    class Meta:
        model = Event
        fields = '__all__'

    def get_joined_patients(self, obj):  # Mettre à jour à `get_joined_patients`
        event_patients = EventPatient.objects.filter(event=obj)
        return EventWorkerSerializer(event_patients, many=True).data

class RewardSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)

    class Meta:
        model = Reward
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['event', 'patient', 'content', 'sentiment', 'created_at']