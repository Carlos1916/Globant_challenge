import logging

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Recover
from backup.models import Backup
from .serializers import RecoverSerializer
from .utils import JobRecover, DepartmentRecover, HiredEmployeeRecover, delete_models
from core.models import Job, Department, HiredEmployee
# Create your views here.

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class RecoverViewSet(APIView):
    def get(self, request):
        logger.info("RecoverView GET called")

        # delete all models
        logger.info("Deleting all models")
        delete_models()
        logger.info("All models deleted")

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
        logger.info("Data recovered")
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

        job_registrations = Job.objects.all().count()
        department_registrations = Department.objects.all().count()
        hired_employee_registrations = HiredEmployee.objects.all().count()
        return Response({"message": "Recovered Data successfully.",
                         "recovered_data": {
                             "job_registrations": job_registrations,
                             "department_registrations": department_registrations,
                             "hired_employee_registrations": hired_employee_registrations
                         },
                         })




