# mental_health_serializers.py

from rest_framework import serializers
from .models import Patient, TreatmentPlan  # Include other relevant models as needed

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'  # Serialize all fields in the Patient model


class TreatmentPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentPlan
        fields = '__all__'  # Serialize all fields in the TreatmentPlan model
