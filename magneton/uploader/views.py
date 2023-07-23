import logging
from io import BytesIO

import boto3
from rest_framework import viewsets
from django.conf import settings

from .models import UploadedFile
from .serializers import UploadedFileSerializer

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Create your views here.
class UploadedFileViewSet(viewsets.ModelViewSet):
    serializer_class = UploadedFileSerializer
    queryset = UploadedFile.objects.all()

    def perform_create(self, serializer):
        logger.info('Attempting to save file')
        serializer.save()
        self.upload_raw_to_s3(serializer.instance)
        self.upload_clean_to_s3(serializer.instance)

    def upload_raw_to_s3(self, instance):
        s3 = boto3.client('s3')

        logger.info('Uploading file to S3')
        logger.info('File name: %s', instance.file.name)

        csv_content = instance.file.read()
        csv_file = BytesIO(csv_content)
        s3.upload_fileobj(
            csv_file,
            settings.AWS_STORAGE_BUCKET_NAME,
            instance.file.name,
            ExtraArgs={
                'ContentType': instance.file_type
            }
        )
        instance.s3_location_raw = f'https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{instance.file.name}'
        logger.info('File %s saved to S3', instance.file.name)
        instance.save()

    def upload_clean_to_s3(self, instance):
        s3 = boto3.client('s3')

        logger.info('Uploading file to S3')
        logger.info('File name: %s', instance.clean_file.name)

        csv_content = instance.clean_file.read()
        csv_file = BytesIO(csv_content)
        s3.upload_fileobj(
            csv_file,
            settings.AWS_STORAGE_BUCKET_NAME,
            instance.clean_file.name,
            ExtraArgs={
                'ContentType': instance.file_type
            }
        )
        instance.s3_location_clean = f'https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{instance.clean_file.name}'
        logger.info('File %s saved to S3', instance.clean_file.name)
        instance.save()


