from django.urls import path
from .views import DepartmentStatView, QuarterStatView

urlpatterns = [
    path('department/', DepartmentStatView.as_view(), name='department-stat'),
    path('quarter/', QuarterStatView.as_view(), name='quarter-stat')
]
