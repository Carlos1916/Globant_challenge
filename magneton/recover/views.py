import logging

from rest_framework.views import APIView
from rest_framework.response import Response


from .models import Recover
from backup.models import Backup
from .serializers import RecoverSerializer
from .utils import JobRecover, DepartmentRecover, HiredEmployeeRecover
# Create your views here.

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class RecoverViewSet(APIView):
    def get(self, request):
        logger.info("RecoverView GET called")
        logger.info("Creating recover")
        # backup files from s3
        backup = Backup.objects.last()
        job_recover = JobRecover(backup.s3_job_location)
        department_recover = DepartmentRecover(backup.s3_department_location)
        hired_employee_recover = HiredEmployeeRecover(backup.s3_hired_employee_location)
        # recover data
        job_recover.recover()
        department_recover.recover()
        hired_employee_recover.recover()
        # create recover object
        recover = Recover.objects.create(
            is_job=True,
            is_department=True,
            is_hired_employee=True,
            job_recover_s3_path=backup.s3_job_location,
            department_recover_s3_path=backup.s3_department_location,
            hired_employee_recover_s3_path=backup.s3_hired_employee_location
        )
        recover.save()
        return Response({"message": "Recover created successfully."})




