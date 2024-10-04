from django.db import models

class Device(models.Model):
    device_name = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    rear_camera_resolution = models.TextField()  # Changed to TextField to accommodate longer text if needed
    front_camera_resolution = models.TextField()  # Changed to TextField for consistency
    operating_system = models.CharField(max_length=255)

    def __str__(self):
        return self.device_name