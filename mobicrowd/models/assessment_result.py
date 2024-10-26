from django.db import models
from .assessment import Assessment  # Import the Assessment model

class AssessmentResult(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    patient_id = models.IntegerField()  # Ideally, replace with a ForeignKey to a Patient model
    results = models.JSONField(help_text="Store assessment results in JSON format.")
    submitted_at = models.DateTimeField(auto_now_add=True)

    # New fields for additional context
    feedback = models.TextField(blank=True, help_text="Provide feedback or insights based on the assessment.")
    follow_up_date = models.DateField(null=True, blank=True, help_text="Date for a follow-up assessment.")
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Reviewed', 'Reviewed')],
        default='Pending',
        help_text="Current status of the assessment results."
    )
    reflections = models.TextField(blank=True, help_text="Patient's reflections or thoughts after the assessment.")
    recommendations = models.TextField(blank=True, help_text="Recommendations for further action or therapy based on results.")

    def __str__(self):
        return f"Results for {self.assessment.title} - Patient ID {self.patient_id}"
