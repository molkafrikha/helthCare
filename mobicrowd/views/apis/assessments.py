from rest_framework import viewsets
from rest_framework.permissions import AllowAny  # Import AllowAny
from mobicrowd.models.assessment import Assessment
from mobicrowd.models.assessment_result import AssessmentResult
from mobicrowd.serializers.assessment_serializers import AssessmentSerializer, AssessmentResultSerializer

class AssessmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing assessments.
    Provides create, retrieve, update, and delete operations.
    Accessible to all users, authenticated or not.
    """
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
    permission_classes = [AllowAny]  # Change to AllowAny

    def perform_create(self, serializer):
        """
        Save the new assessment instance after adding any custom logic, if needed.
        """
        serializer.save()

class AssessmentResultViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing assessment results.
    Provides create and retrieve operations.
    Accessible to all users, authenticated or not.
    """
    queryset = AssessmentResult.objects.all()
    serializer_class = AssessmentResultSerializer
    permission_classes = [AllowAny]  # Change to AllowAny

    def perform_create(self, serializer):
        """
        Save the new assessment result instance after adding any custom logic, if needed.
        """
        serializer.save()
