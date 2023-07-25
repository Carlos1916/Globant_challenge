import avro.schema
import avro.io
from avro.datafile import DataFileWriter
from io import BytesIO


# class DepartmentAvroSerializer:
#     schema = avro.schema.parse("""
#         {
#             "type": "record",
#             "name": "Department",
#             "fields": [
#                 {"name": "id", "type": "int"},
#                 {"name": "department", "type": "string"}
#             ]
#         }
#     """)
#
#     @classmethod
#     def serialize_list(cls, departments):
#         writer = avro.io.DatumWriter(cls.schema)
#         bytes_writer = BytesIO()
#         encoder = avro.io.BinaryEncoder(bytes_writer)
#         for department in departments:
#             record = {"id": department._id, "department": department.department}
#             writer.write(record, encoder)
#         return bytes_writer.getvalue()
#
#     @staticmethod
#     def record_return(record: dict):
#         return {"id_": record['id'], "department": record['department']}
#
#
# class JobAvroSerializer:
#     schema = avro.schema.parse("""
#         {
#             "type": "record",
#             "name": "Job",
#             "fields": [
#                 {"name": "id", "type": "int"},
#                 {"name": "job", "type": "string"}
#             ]
#         }
#     """)
#
#     @classmethod
#     def serialize_list(cls, jobs):
#         writer = avro.io.DatumWriter(cls.schema)
#         bytes_writer = BytesIO()
#         encoder = avro.io.BinaryEncoder(bytes_writer)
#         for job in jobs:
#             record = {"id": job._id, "job": job.job}
#             writer.write(record, encoder)
#         return bytes_writer.getvalue()
#
#     @staticmethod
#     def record_return(record: dict):
#         return {"id_": record['id'], "job": record['job']}
#
#
# class HiredEmployeeAvroSerializer:
#     schema = avro.schema.parse("""
#         {
#             "type": "record",
#             "name": "HiredEmployee",
#             "fields": [
#                 {"name": "id", "type": "int"},
#                 {"name": "datetime", "type": "string"},
#                 {
#                     "name": "department",
#                     "type": ["null", {
#                         "type": "record",
#                         "name": "Department",
#                         "fields": [
#                             {"name": "id", "type": "int"},
#                             {"name": "department", "type": "string"}
#                         ]
#                     }],
#                     "default": null
#                 },
#                 {
#                     "name": "job",
#                     "type": ["null", {
#                         "type": "record",
#                         "name": "Job",
#                         "fields": [
#                             {"name": "id", "type": "int"},
#                             {"name": "job", "type": "string"}
#                         ]
#                     }],
#                     "default": null
#                 }
#             ]
#         }
#     """)
#
#     @classmethod
#     def serialize_list(cls, hired_employees):
#         writer = avro.io.DatumWriter(cls.schema)
#         bytes_writer = BytesIO()
#         encoder = avro.io.BinaryEncoder(bytes_writer)
#         for he in hired_employees:
#             record = {
#                 "id": he._id,
#                 "datetime": he.datetime,
#                 "department": {
#                     "id": he.department._id,
#                     "department": he.department.department,
#                 },
#                 "job": {
#                     "id": he.job._id,
#                     "job": he.job.job,
#                 },
#             }
#             writer.write(record, encoder)
#         return bytes_writer.getvalue()
#
#     # @staticmethod
#     # def record_return(record: dict):
#     #     return {
#     #         "id_": record['id'],
#     #         "datetime": record['datetime'],
#     #         "department": record['department']

# class AvroSerializer:
#     def __init__(self, schema: str):
#         self.schema =
#
#     def serialize_list(self, objects):
#
#
#     def record_return(self, record: dict):
#         raise NotImplementedError

