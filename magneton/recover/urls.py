from django.urls import path
from .views import RecoverViewSet

urlpatterns = [
    path('recover/', RecoverViewSet.as_view(), name='recover-view'),
]
