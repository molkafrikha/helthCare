from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = True


# this class store image of admin , student , teacher in a folder entitled with the name of the user
from storages.backends.s3boto3 import S3Boto3Storage

class CustomS3Boto3Storage(S3Boto3Storage):
    def __init__(self, folder_name='', dynamic_folder_name='', *args, **kwargs):
        self.folder_name = folder_name
        self.dynamic_folder_name = dynamic_folder_name
        # Remove ACL from kwargs if it's being passed
        kwargs.pop('default_acl', None)
        super().__init__(*args, **kwargs)

    def get_available_name(self, name, max_length=1500):
        folder_name = self.folder_name
        dynamic_folder_name = self.dynamic_folder_name
        name_parts = name.split('/')
        new_name = f"{folder_name}/{dynamic_folder_name}/{name_parts[-1]}"
        return super().get_available_name(new_name, max_length)

    def set_dynamic_folder_name(self, dynamic_folder_name):
        self.dynamic_folder_name = dynamic_folder_name

    def set_folder_name(self, folder_name):
        self.folder_name = folder_name
