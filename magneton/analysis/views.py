from rest_framework.views import APIView
from rest_framework.response import Response

from .utils import run_sql_query, quarter_query, department_query
# Create your views here.


class DepartmentStatView(APIView):
    def get(self, request, format=None):
        rows = run_sql_query(department_query)
        data = []
        for row in rows:
            data.append(
                {
                    "id": row[0],
                    "department": row[1],
                    "hired": row[2]
                }
            )
        return Response(data)


class QuarterStatView(APIView):
    def get(self, request, format=None):
        rows = run_sql_query(quarter_query)
        data = []
        for row in rows:
            data.append(
                {
                    "department": row[0],
                    "job": row[1],
                    "Q1": row[2],
                    "Q2": row[3],
                    "Q3": row[4],
                    "Q4": row[5]
                }
            )
        return Response(data)
