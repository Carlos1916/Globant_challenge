from rest_framework import serializers

from .models import Job, HiredEmployee, Department


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'


class HiredEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HiredEmployee
        fields = '__all__'