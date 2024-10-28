# Generated by Django 5.0.6 on 2024-10-28 10:43

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('fullName', models.CharField(max_length=255)),
                ('mobile_phone', models.CharField(max_length=20)),
                ('is_doctor', models.BooleanField(default=False)),
                ('is_patient', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('role', models.CharField(choices=[('Patient', 'Patient'), ('Doctor', 'Doctor'), ('Admin', 'Admin')], max_length=20)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': 'Custom Users',
            },
        ),
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_assessment', models.DateField(auto_now_add=True, help_text='Date of the assessment.')),
                ('mood_rating', models.IntegerField(choices=[(1, 'Very Low'), (2, 'Low'), (3, 'Neutral'), (4, 'High'), (5, 'Very High')], default=3, help_text='Rate your mood on a scale from 1 (Very Low) to 5 (Very High).')),
                ('anxiety_rating', models.IntegerField(choices=[(1, 'Very Low'), (2, 'Low'), (3, 'Neutral'), (4, 'High'), (5, 'Very High')], default=3, help_text='Rate your anxiety level on a scale from 1 (Very Low) to 5 (Very High).')),
                ('stress_rating', models.IntegerField(choices=[(1, 'Very Low'), (2, 'Low'), (3, 'Neutral'), (4, 'High'), (5, 'Very High')], default=3, help_text='Rate your stress level on a scale from 1 (Very Low) to 5 (Very High).')),
                ('sleep_quality_rating', models.IntegerField(choices=[(1, 'Very Poor'), (2, 'Poor'), (3, 'Fair'), (4, 'Good'), (5, 'Excellent')], default=3, help_text='Rate the quality of your sleep on a scale from 1 (Very Poor) to 5 (Excellent).')),
                ('physical_pain_rating', models.IntegerField(choices=[(1, 'None'), (2, 'Mild'), (3, 'Moderate'), (4, 'Severe'), (5, 'Extreme')], default=1, help_text='Rate your physical pain level today on a scale from 1 (None) to 5 (Extreme).')),
                ('coping_mechanisms', models.TextField(blank=True, default='No coping mechanisms reported.', help_text='Describe any coping strategies you use to manage stress and anxiety.')),
                ('recent_events', models.TextField(blank=True, default='No recent events reported.', help_text='Describe any recent life events that may have impacted your mental health.')),
                ('daily_highlights', models.TextField(blank=True, help_text='List any positive experiences or highlights from today.')),
                ('thought_patterns', models.TextField(blank=True, default='No specific thoughts reported.', help_text='Describe any persistent thoughts or patterns (negative or positive) you experienced today.')),
                ('gratitude_entries', models.TextField(blank=True, help_text='List things you are grateful for today.')),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_name', models.CharField(max_length=255)),
                ('manufacturer', models.CharField(max_length=255)),
                ('rear_camera_resolution', models.TextField()),
                ('front_camera_resolution', models.TextField()),
                ('operating_system', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('location', models.JSONField(default=dict)),
                ('cost', models.FloatField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('deadline', models.DateTimeField()),
                ('startdate', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='doctor_profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('specialty', models.CharField(max_length=255, null=True)),
                ('qualifications', models.TextField(null=True)),
                ('availability', models.JSONField(default=list, null=True)),
                ('consultation_fee', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='doctor_pics/')),
                ('approved', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='patient_profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('date_of_birth', models.DateField()),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('medical_history', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AssessmentResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_id', models.IntegerField()),
                ('results', models.JSONField(help_text='Store assessment results in JSON format.')),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('feedback', models.TextField(blank=True, help_text='Provide feedback or insights based on the assessment.')),
                ('follow_up_date', models.DateField(blank=True, help_text='Date for a follow-up assessment.', null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Reviewed', 'Reviewed')], default='Pending', help_text='Current status of the assessment results.', max_length=20)),
                ('reflections', models.TextField(blank=True, help_text="Patient's reflections or thoughts after the assessment.")),
                ('recommendations', models.TextField(blank=True, help_text='Recommendations for further action or therapy based on results.')),
                ('reviewed_by', models.CharField(blank=True, help_text='Name of the reviewer or therapist who reviewed the assessment results.', max_length=100)),
                ('review_date', models.DateField(blank=True, help_text='Date when the assessment results were reviewed.', null=True)),
                ('urgency_level', models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], default='Low', help_text='Indicate the urgency level based on the assessment results.', max_length=10)),
                ('additional_notes', models.TextField(blank=True, help_text='Any additional notes or remarks about the assessment results.')),
                ('flagged_for_follow_up', models.BooleanField(default=False, help_text='Indicate if this result is flagged for a mandatory follow-up.')),
                ('assessment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mobicrowd.assessment')),
            ],
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.CharField(max_length=100)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rewards_list', to='mobicrowd.event')),
            ],
        ),
        migrations.CreateModel(
            name='PatientReward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('awarded_on', models.DateTimeField(auto_now_add=True)),
                ('reward', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reward_patients', to='mobicrowd.reward')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_rewards', to='mobicrowd.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='mobicrowd.doctor'),
        ),
        migrations.AddField(
            model_name='reward',
            name='patients',
            field=models.ManyToManyField(related_name='reward_list', through='mobicrowd.PatientReward', to='mobicrowd.patient'),
        ),
        migrations.CreateModel(
            name='EventPatient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')], default='PENDING', max_length=50)),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mobicrowd.event')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mobicrowd.patient')),
            ],
            options={
                'unique_together': {('event', 'patient')},
            },
        ),
        migrations.AddField(
            model_name='event',
            name='joined_patients',
            field=models.ManyToManyField(blank=True, related_name='joined_events', through='mobicrowd.EventPatient', to='mobicrowd.patient'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('sentiment', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='mobicrowd.event')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mobicrowd.patient')),
            ],
        ),
    ]
