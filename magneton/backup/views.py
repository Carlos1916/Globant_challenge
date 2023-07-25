import logging
import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings

from .models import Backup
from .utils import AvroWriter, department_avro_schema, hired_employees_avro_schema, job_avro_schema
from .utils import create_hired_employees_records as cher
from core.models import Job, HiredEmployee, Department

# Create your views here.

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class BackupView(APIView):
    def get(self, request):
        logger.info("BackupView GET called")
        logger.info("Creating backup")
        departments = list(Department.objects.all().values())
        jobs = list(Job.objects.all().values())
        hired_employees = cher(HiredEmployee.objects.select_related('department', 'job').all())

        logger.info("Creating AvroWriter objects")
        department_data = AvroWriter(departments, department_avro_schema)
        job_data = AvroWriter(jobs, job_avro_schema)
        hired_employee_data = AvroWriter(hired_employees, hired_employees_avro_schema)

        logger.info("Creating S3 keys")
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        time_format = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        department_s3_key = f'backup/department/{time_format}_department_backup.avro'
        job_s3_key = f'backup/job/{time_format}_job_backup.avro'
        hired_employee_s3_key = f'backup/hired_employee/{time_format}_hired_employee_backup.avro'

        logger.info("Writing and dumping data")
        department_data.write_and_dump(bucket_name, department_s3_key)
        job_data.write_and_dump(bucket_name, job_s3_key)
        hired_employee_data.write_and_dump(bucket_name, hired_employee_s3_key)
        logger.info("Data written and dumped")

        logger.info("Creating Backup object")
        backup = Backup.objects.create(
            is_job=True,
            is_department=True,
            is_hired_employee=True,
            s3_job_location=f"s3://{bucket_name}/{job_s3_key}",
            s3_department_location=f"s3://{bucket_name}/{department_s3_key}",
            s3_hired_employee_location=f"s3://{bucket_name}/{hired_employee_s3_key}"
        )
        backup.save()
        return Response({"message": "Backup created successfully."})
