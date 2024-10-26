# assessment_serializers.py

from rest_framework import serializers
from mobicrowd.models.assessment import Assessment
from mobicrowd.models.assessment_result import AssessmentResult
class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = '__all__'  # This will serialize all fields in the Assessment model


class AssessmentResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentResult
        fields = '__all__'  # This will serialize all fields in the AssessmentResult model
