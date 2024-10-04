# serializers.py
from rest_framework import serializers

from mobicrowd.models.device_cam_specs import Device


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'