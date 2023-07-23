from rest_framework import serializers
from .models import UploadedFile


class UploadedFileSerializer(serializers.ModelSerializer):
    clean_file = serializers.FileField(read_only=True)

    class Meta:
        model = UploadedFile
        fields = ['id', 'file', 'uploaded_at', 'clean_file']
        read_only_fields = ['s3_location_clean', 'file_type', 'file_table', 's3_location_raw']

