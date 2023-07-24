from django.db import models

# Create your models here.


class Backup(models.Model):
    # Backup model to store data in Avro format from Job, HiredEmployees and Department tables

    id = models.AutoField(primary_key=True)
    is_job = models.BooleanField()
    is_hired_employee = models.BooleanField()
    is_department = models.BooleanField()
    backup_timestamp = models.DateTimeField(auto_now_add=True)
    s3_job_location = models.CharField(max_length=200, blank=True, null=True)
    s3_hired_employee_location = models.CharField(max_length=200, blank=True, null=True)
    s3_department_location = models.CharField(max_length=200, blank=True, null=True)



