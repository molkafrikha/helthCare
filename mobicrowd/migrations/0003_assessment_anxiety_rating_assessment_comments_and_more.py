# Generated by Django 5.0.6 on 2024-10-26 22:45

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobicrowd', '0002_assessment_assessmentresult'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessment',
            name='anxiety_rating',
            field=models.IntegerField(choices=[(1, 'Very Low'), (2, 'Low'), (3, 'Neutral'), (4, 'High'), (5, 'Very High')], default=3, help_text='Rate your anxiety level on a scale from 1 (Very Low) to 5 (Very High).'),
        ),
        migrations.AddField(
            model_name='assessment',
            name='comments',
            field=models.TextField(blank=True, help_text='Additional comments or notes.'),
        ),
        migrations.AddField(
            model_name='assessment',
            name='coping_mechanisms',
            field=models.TextField(default='No coping mechanisms reported.', help_text='Describe any coping strategies you use to manage stress and anxiety.'),
        ),
        migrations.AddField(
            model_name='assessment',
            name='date_of_assessment',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='assessment',
            name='follow_up_needed',
            field=models.BooleanField(default=False, help_text='Indicate if follow-up is needed after this assessment.'),
        ),
        migrations.AddField(
            model_name='assessment',
            name='mood_rating',
            field=models.IntegerField(choices=[(1, 'Very Low'), (2, 'Low'), (3, 'Neutral'), (4, 'High'), (5, 'Very High')], default=3, help_text='Rate your mood on a scale from 1 (Very Low) to 5 (Very High).'),
        ),
        migrations.AddField(
            model_name='assessment',
            name='recent_events',
            field=models.TextField(blank=True, default='No recent events reported.', help_text='Describe any recent life events that may have impacted your mental health.'),
        ),
        migrations.AddField(
            model_name='assessment',
            name='stress_rating',
            field=models.IntegerField(choices=[(1, 'Very Low'), (2, 'Low'), (3, 'Neutral'), (4, 'High'), (5, 'Very High')], default=3, help_text='Rate your stress level on a scale from 1 (Very Low) to 5 (Very High).'),
        ),
        migrations.AddField(
            model_name='assessmentresult',
            name='feedback',
            field=models.TextField(blank=True, help_text='Provide feedback or insights based on the assessment.'),
        ),
        migrations.AddField(
            model_name='assessmentresult',
            name='follow_up_date',
            field=models.DateField(blank=True, help_text='Date for a follow-up assessment.', null=True),
        ),
        migrations.AddField(
            model_name='assessmentresult',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Reviewed', 'Reviewed')], default='Pending', help_text='Current status of the assessment results.', max_length=20),
        ),
        migrations.AlterField(
            model_name='assessmentresult',
            name='results',
            field=models.JSONField(help_text='Store assessment results in JSON format.'),
        ),
    ]