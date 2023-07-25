from django.db import models

# Create your models here.


class Department(models.Model):
    id = models.AutoField(primary_key=True)
    _id = models.IntegerField(blank=True, null=True)
    department = models.CharField(max_length=50, blank=True, null=True, default='')

    def __str__(self):
        return f"{self.id} - {self.department}"


class Job(models.Model):
    id = models.AutoField(primary_key=True)
    _id = models.IntegerField(blank=True, null=True)
    job = models.CharField(max_length=50, blank=True, null=True, default='')

    def __str__(self):
        return f"{self.id} - {self.job}"


class HiredEmployee(models.Model):
    id = models.AutoField(primary_key=True)
    _id = models.IntegerField(blank=True, null=True)
    datetime = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.id} - {self.datetime} - {self.department} - {self.job}"