from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
import os
from django_filters.rest_framework import DjangoFilterBackend
from mobicrowd.models.device_cam_specs import Device
from mobicrowd.serializers.deviceCamSpecsSerializers import DeviceSerializer
from django_filters import rest_framework as filters
from rest_framework import generics
@api_view(['POST'])
def upload_devices_file(request):
    # Define the local path to the JSON file
    file_path = 'scraping/formatted_camera_specs.json'

    if not os.path.exists(file_path):
        return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        with open(file_path, 'r') as file:
            devices_data = json.load(file)  # Use json.load() to parse the entire file as a JSON array
    except json.JSONDecodeError:
        return Response({'error': 'Invalid JSON format'}, status=status.HTTP_400_BAD_REQUEST)

    # Transform the data to match the serializer fields
    transformed_data = []
    for device in devices_data:
        transformed_device = {
            'device_name': device.get('device_name'),
            'manufacturer': device.get('manufacturer'),
            'rear_camera_resolution': device.get('rear_camera', {}).get('resolution'),
            'front_camera_resolution': device.get('front_camera', {}).get('resolution'),
            'operating_system': device.get('operating_system')
        }
        transformed_data.append(transformed_device)

    # Convert the data to a list of devices
    serializer = DeviceSerializer(data=transformed_data, many=True)

    if serializer.is_valid():
        serializer.save()
        return Response(f"{len(serializer.data)} mobile specs inserted", status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# filters.py


class DeviceFilter(filters.FilterSet):
    device_name = filters.CharFilter(lookup_expr='icontains')
    manufacturer = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Device
        fields = ['device_name', 'manufacturer']

class DeviceListView(generics.ListAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DeviceFilter