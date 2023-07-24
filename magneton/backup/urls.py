from django.urls import path
from .views import BackupView

urlpatterns = [
    path('backup/', BackupView.as_view(), name='backup-view'),
]
