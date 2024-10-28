from django.db import models
from django.utils import timezone
from mobicrowd.models.Users import Patient , Doctor

class Event(models.Model):
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.JSONField(default=dict)  # Store location as a JSON dictionary
    cost = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)
    deadline = models.DateTimeField()
    startdate = models.DateTimeField()
    joined_patients = models.ManyToManyField('Patient', through='EventPatient', related_name='joined_events', blank=True)

    def __str__(self):
        return self.title

class EventPatient(models.Model):
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=PENDING)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'patient')

class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=False)
    content = models.TextField()  # Contenu du commentaire
    sentiment = models.TextField(blank=True, null=True)  # Champ pour le sentiment (généré automatiquement)
    created_at = models.DateTimeField(default=timezone.now)  # Date de création

    def __str__(self):
        return f'Comment by {self.patient} on {self.event} at {self.created_at}'

class Reward(models.Model):
    cost = models.CharField(max_length=100)
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='rewards_list')
    patients = models.ManyToManyField('Patient', through='PatientReward', related_name='reward_list')

class PatientReward(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='patient_rewards')
    reward = models.ForeignKey('Reward', on_delete=models.CASCADE, related_name='reward_patients')
    awarded_on = models.DateTimeField(auto_now_add=True)
