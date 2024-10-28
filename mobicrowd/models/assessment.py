from django.db import models

class Assessment(models.Model):
    # Patient-submitted information
    date_of_assessment = models.DateField(auto_now_add=True, help_text="Date of the assessment.")
    
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
    
    # Additional Ratings
    sleep_quality_rating = models.IntegerField(
        choices=[(1, 'Very Poor'), (2, 'Poor'), (3, 'Fair'), (4, 'Good'), (5, 'Excellent')],
        default=3,
        help_text="Rate the quality of your sleep on a scale from 1 (Very Poor) to 5 (Excellent)."
    )
    physical_pain_rating = models.IntegerField(
        choices=[(1, 'None'), (2, 'Mild'), (3, 'Moderate'), (4, 'Severe'), (5, 'Extreme')],
        default=1,
        help_text="Rate your physical pain level today on a scale from 1 (None) to 5 (Extreme)."
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
    daily_highlights = models.TextField(
        blank=True,
        help_text="List any positive experiences or highlights from today."
    )
    thought_patterns = models.TextField(
        blank=True,
        default="No specific thoughts reported.",
        help_text="Describe any persistent thoughts or patterns (negative or positive) you experienced today."
    )
    gratitude_entries = models.TextField(
        blank=True,
        help_text="List things you are grateful for today."
    )

    def __str__(self):
        return f"Assessment on {self.date_of_assessment}"