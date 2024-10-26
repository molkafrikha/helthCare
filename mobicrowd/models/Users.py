from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **otherfields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            **otherfields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **otherfields):
        user = self.create_user(
            email,
            password=password,
            **otherfields
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    fullName = models.CharField(max_length=255)
    mobile_phone = models.CharField(max_length=20)
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=(('Patient', 'Patient'), ('Doctor', 'Doctor'), ('Admin', 'Admin')))
    objects = UserManager()
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullName', 'mobile_phone']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.fullName}"

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_admin(self):
        return self.is_superuser

    class Meta:
        verbose_name_plural = "Custom Users"


class Token(models.Model):
    token = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='doctor_profile')
    specialty = models.CharField(max_length=255,null=True)
    qualifications = models.TextField(null=True)
    availability = models.JSONField(default=list ,null=True)  # e.g., [{"day": "Monday", "time": "09:00-17:00"}]
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2 ,null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='doctor_pics/', blank=True, null=True)
    approved = models.BooleanField(default=True)  # Add this line
    def __str__(self):
        return f"Dr. {self.user.fullName} -  {self.specialty}"


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='patient_profile')
    date_of_birth = models.DateField()
    #gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.fullName
