import avro.schema
import avro.io
from avro.datafile import DataFileWriter
from io import BytesIO


class DepartmentAvroSerializer:
    schema = avro.schema.parse("""
        {
            "type": "record",
            "name": "Department",
            "fields": [
                {"name": "id", "type": "int"},
                {"name": "department", "type": "string"}
            ]
        }
    """)

    @classmethod
    def serialize_list(cls, departments):
        writer = avro.io.DatumWriter(cls.schema)
        bytes_writer = BytesIO()
        encoder = avro.io.BinaryEncoder(bytes_writer)
        for department in departments:
            record = {"id": department.id, "department": department.department}
            writer.write(record, encoder)
        return bytes_writer.getvalue()


class JobAvroSerializer:
    schema = avro.schema.parse("""
        {
            "type": "record",
            "name": "Job",
            "fields": [
                {"name": "id", "type": "int"},
                {"name": "job", "type": "string"}
            ]
        }
    """)

    @classmethod
    def serialize_list(cls, jobs):
        writer = avro.io.DatumWriter(cls.schema)
        bytes_writer = BytesIO()
        encoder = avro.io.BinaryEncoder(bytes_writer)
        for job in jobs:
            record = {"id": job.id, "job": job.job}
            writer.write(record, encoder)
        return bytes_writer.getvalue()


class HiredEmployeeAvroSerializer:
    schema = avro.schema.parse("""
        {
            "type": "record",
            "name": "HiredEmployee",
            "fields": [
                {"name": "id", "type": "int"},
                {"name": "datetime", "type": "string"},
                {
                    "name": "department",
                    "type": ["null", {
                        "type": "record",
                        "name": "Department",
                        "fields": [
                            {"name": "id", "type": "int"},
                            {"name": "department", "type": "string"}
                        ]
                    }],
                    "default": null
                },
                {
                    "name": "job",
                    "type": ["null", {
                        "type": "record",
                        "name": "Job",
                        "fields": [
                            {"name": "id", "type": "int"},
                            {"name": "job", "type": "string"}
                        ]
                    }],
                    "default": null
                }
            ]
        }
    """)

    @classmethod
    def serialize_list(cls, hired_employees):
        writer = avro.io.DatumWriter(cls.schema)
        bytes_writer = BytesIO()
        encoder = avro.io.BinaryEncoder(bytes_writer)
        for he in hired_employees:
            record = {
                "id": he.id,
                "datetime": he.datetime,
                "department": {
                    "id": he.department.id,
                    "department": he.department.department,
                },
                "job": {
                    "id": he.job.id,
                    "job": he.job.job,
                },
            }
            writer.write(record, encoder)
        return bytes_writer.getvalue()
