from django.urls import path, include
from rest_framework import routers
from .views import UploadedFileViewSet

router = routers.DefaultRouter()
router.register(r'upload', UploadedFileViewSet, basename='upload')

urlpatterns = [
    path('api/', include(router.urls)),
]
