from django.shortcuts import render
from .serializers import RecoverSerializer
from rest_framework import viewsets
from .models import Recover
# Create your views here.


class RecoverViewSet(viewsets.ModelViewSet):
    serializer_class = RecoverSerializer
    queryset = Recover.objects.all()

