from django.db import models
from .assessment import Assessment  # Import the Assessment model

class AssessmentResult(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    patient_id = models.IntegerField()  # Replace with actual patient identification logic
    results = models.JSONField()  # Store assessment results as JSON
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Results for {self.assessment.title} - Patient ID {self.patient_id}"
