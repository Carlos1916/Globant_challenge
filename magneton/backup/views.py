import logging
import datetime

import boto3
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Backup
from core.models import Job, HiredEmployee, Department
from core.avro_serializers import DepartmentAvroSerializer, JobAvroSerializer, HiredEmployeeAvroSerializer
# Create your views here.

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class BackupView(APIView):
    def get(self, request):
        departments = Department.objects.all()
        jobs = Job.objects.all()
        hired_employees = HiredEmployee.objects.all()

        department_data = DepartmentAvroSerializer.serialize_list(departments)
        job_data = JobAvroSerializer.serialize_list(jobs)
        hired_employee_data = HiredEmployeeAvroSerializer.serialize_list(hired_employees)

        s3 = boto3.resource('s3')
        bucket_name = 'magneton-app'
        time_format = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        department_s3_key = f'backup/department/{time_format}_backup.avro'
        s3.Object(bucket_name, department_s3_key).put(Body=department_data)

        job_s3_key = f'backup/job/{time_format}_backup.avro'
        s3.Object(bucket_name, job_s3_key).put(Body=job_data)

        hired_employee_s3_key = f'backup/hired_employee/{time_format}_backup.avro'
        s3.Object(bucket_name, hired_employee_s3_key).put(Body=hired_employee_data)

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
