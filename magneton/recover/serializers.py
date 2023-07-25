from rest_framework import serializers
from .models import Recover


class RecoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recover
        fields = '__all__'
