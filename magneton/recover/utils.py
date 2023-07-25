import io

import boto3
import fastavro
from botocore.exceptions import ClientError

from core.models import Job, Department, HiredEmployee


def parse_s3_uri(s3_uri):
    if not s3_uri.startswith('s3://'):
        raise ValueError("Invalid S3 URI. It should start with 's3://'")

    s3_path = s3_uri[5:]  # Remove 's3://' from the URI
    bucket, key = s3_path.split('/', 1)  # Split by the first occurrence of '/'

    return bucket, key


def get_data_from_avro(s3_bucket, s3_key):
    s3_client = boto3.client('s3')

    # Download the Avro file from S3
    response = s3_client.get_object(Bucket=s3_bucket, Key=s3_key)
    avro_data = response['Body'].read()

    # Create an Avro reader
    avro_data = list(fastavro.reader(io.BytesIO(avro_data)))

    return avro_data


def delete_models():
    Job.objects.all().delete()
    Department.objects.all().delete()
    HiredEmployee.objects.all().delete()


class JobRecover:
    def __init__(self, s3_job_location):
        self.s3_job_location = s3_job_location
        self.data = None

    def recover(self):
        bucket, key = parse_s3_uri(self.s3_job_location)
        self.data = get_data_from_avro(bucket, key)
        self.save()

    def dictionary_builder(self):
        job_list = []
        for job in self.data:
            data_dict = {
                '_id': job['_id'],
                'job': job['job'],
            }
            job_list.append(data_dict)
        return job_list

    def save(self):
        job_list = self.dictionary_builder()
        for i in job_list:
            job_instance, created = Job.objects.get_or_create(**i)
            if not created:
                job_instance._id = i['_id']
                job_instance.job = i['job']
                job_instance.save()


class DepartmentRecover:
    def __init__(self, s3_department_location):
        self.s3_department_location = s3_department_location
        self.data = None

    def recover(self):
        bucket, key = parse_s3_uri(self.s3_department_location)
        self.data = get_data_from_avro(bucket, key)
        self.save()

    def dictionary_builder(self):
        department_list = []
        for dep in self.data:
            dep_data = {
                '_id': dep['_id'],
                'department': dep['department'],
            }
            department_list.append(dep_data)
        return department_list

    def save(self):
        department_list = self.dictionary_builder()
        for i in department_list:
            department_instance, created = Department.objects.get_or_create(**i)
            if not created:
                department_instance._id = i['_id']
                department_instance.department = i['department']
                department_instance.save()


class HiredEmployeeRecover:
    def __init__(self, s3_hired_employee_location):
        self.s3_hired_employee_location = s3_hired_employee_location
        self.data = None

    def recover(self):
        bucket, key = parse_s3_uri(self.s3_hired_employee_location)
        self.data = get_data_from_avro(bucket, key)
        self.save()

    def dictionary_builder(self):
        hired_employee_list = []
        for he in self.data:
            department_instance, _ = Department.objects.get_or_create(_id=he['department']['_id'])
            job_instance, _ = Job.objects.get_or_create(_id=he['job']['_id'])

            he_data = {
                '_id': he['_id'],
                'datetime': he['datetime'],
                'department': department_instance,
                'job': job_instance,
            }
            hired_employee_list.append(he_data)
        return hired_employee_list

    def save(self):
        hired_employee_list = self.dictionary_builder()
        for i in hired_employee_list:
            hired_employee_instance, created = HiredEmployee.objects.get_or_create(_id=i['_id'])
            if not created:
                hired_employee_instance._id = i['_id']
                hired_employee_instance.datetime = i['datetime']
                hired_employee_instance.department = i['department']
                hired_employee_instance.job = i['job']
                hired_employee_instance.save()
