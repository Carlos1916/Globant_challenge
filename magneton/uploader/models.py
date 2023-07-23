import os
import logging
import datetime

import pandas as pd
import boto3

from django.db import models

from .utils import get_upload_path, clean_csv, assign_schema
from core.models import Department, Job, HiredEmployee

# Create your models here.

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class UploadedFile(models.Model):
    FILE_TYPE_CHOICES = [
        ('csv', 'CSV'),
        ('parquet', 'Parquet'),
        ('avro', 'Avro'),
    ]

    FILE_TABLE = [
        ('departments', 'Departments'),
        ('hired_employees', 'Employees'),
        ('jobs', 'Jobs'),
    ]

    file = models.FileField(upload_to=get_upload_path)
    clean_file = models.FileField(upload_to='upload/clean/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_table = models.CharField(max_length=20, choices=FILE_TABLE, default='hired_employees')
    s3_location_clean = models.CharField(max_length=20, blank=True, null=True)
    s3_location_raw = models.CharField(max_length=20, blank=True, null=True)
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES, default='csv')

    def save(self, *args, **kwargs):
        self.file_type = self.file.name.split('.')[-1]
        self.file_table = self.get_file_table()
        if self.file and not self.clean_file:
            clean_df = self.process_file()
            logger.info('Saving clean file')
            self.clean_file = self.save_cleaned_file(clean_df)
            logger.info('Uploading data to core tables')
            self.upload_core_tables_from_csv(clean_df)
            super().save(*args, **kwargs)

    def get_file_table(self):
        filename = os.path.basename(self.file.name).lower()

        for choice_value, choice_label in self.FILE_TABLE:
            if choice_value in filename:
                return choice_value

        return 'hired_employees'

    def process_file(self):
        schema = assign_schema(self)
        clean_df = clean_csv(self.file, schema, self)
        return clean_df

    def save_cleaned_file(self, clean_df):
        cleaned_file_directory = f'media/uploads/clean/{self.file_type}/{self.file_table}/'
        # create directory if not exists
        if not os.path.exists(cleaned_file_directory):
            os.makedirs(cleaned_file_directory)

        file_name = f'{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}_{self.file.name.split("/")[-1]}'
        clean_df.to_csv(f'{cleaned_file_directory}{file_name}', index=False)
        corrected_path = cleaned_file_directory.replace('media/', '')
        return f'{corrected_path}{file_name}'

    def upload_core_tables_from_csv(self, df):

        # Iterate over each row to create instance depending on table_name
        if self.file_table == 'hired_employees':
            logger.info('Uploading hired_employee table')
            for index, row in df.iterrows():
                hired_employee, _ = HiredEmployee.objects.get_or_create(id=int(row['id']))
                hired_employee.datetime = row['datetime']

                hired_employee.department = Department.objects.get(id=int(row['department_id']))
                hired_employee.job = Job.objects.get(id=int(row['job_id']))
                hired_employee.save()
        elif self.file_table == 'departments':
            logger.info('Uploading department table')
            for index, row in df.iterrows():
                department, _ = Department.objects.get_or_create(id=int(row['id']))
                department.department = row['department']
                department.save()
        elif self.file_table == 'jobs':
            logger.info('Uploading job table')
            for index, row in df.iterrows():
                job, _ = Job.objects.get_or_create(id=int(row['id']))
                job.job = row['job']
                job.save()
        else:
            logger.info(f'No table found for {self.file_table}')

    def read_from_s3_location(self):
        # read the clean file from s3
        pass


