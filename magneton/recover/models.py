from django.db import models

# Create your models here.


class Recover(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_job = models.BooleanField(default=False)
    is_hired_employee = models.BooleanField(default=False)
    is_department = models.BooleanField(default=False)
    job_recover_s3_path = models.CharField(max_length=255, blank=True, null=True)
    hired_employee_recover_s3_path = models.CharField(max_length=255, blank=True, null=True)
    department_recover_s3_path = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Recover {self.id}"
