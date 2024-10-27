from django.db import models
from django.utils import timezone

class Assessment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(help_text="Brief description of the assessment purpose.")
    created_at = models.DateTimeField(auto_now_add=True)

    # Patient-submitted information
    date_of_assessment = models.DateField(default=timezone.now, help_text="Date of the assessment.")
    
    # Ratings submitted by the patient
    mood_rating = models.IntegerField(
        choices=[(1, 'Very Low'), (2, 'Low'), (3, 'Neutral'), (4, 'High'), (5, 'Very High')],
        default=3,
        help_text="Rate your mood on a scale from 1 (Very Low) to 5 (Very High)."
    )
    anxiety_rating = models.IntegerField(
        choices=[(1, 'Very Low'), (2, 'Low'), (3, 'Neutral'), (4, 'High'), (5, 'Very High')],
        default=3,
        help_text="Rate your anxiety level on a scale from 1 (Very Low) to 5 (Very High)."
    )
    stress_rating = models.IntegerField(
        choices=[(1, 'Very Low'), (2, 'Low'), (3, 'Neutral'), (4, 'High'), (5, 'Very High')],
        default=3,
        help_text="Rate your stress level on a scale from 1 (Very Low) to 5 (Very High)."
    )
    
    # Open-ended fields for patient input
    coping_mechanisms = models.TextField(
        blank=True,
        default="No coping mechanisms reported.",
        help_text="Describe any coping strategies you use to manage stress and anxiety."
    )
    recent_events = models.TextField(
        blank=True,
        default="No recent events reported.",
        help_text="Describe any recent life events that may have impacted your mental health."
    )
    follow_up_needed = models.BooleanField(default=False, help_text="Indicate if follow-up is needed after this assessment.")
    comments = models.TextField(blank=True, help_text="Additional comments or notes about your assessment.")

    def __str__(self):
        return self.title
