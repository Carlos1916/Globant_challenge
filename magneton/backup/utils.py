import io
import fastavro
import boto3

department_avro_schema = {
  "type": "record",
  "name": "Department",
  "fields": [
    {"name": "_id", "type": "int"},
    {"name": "department", "type": "string", "default": ""}
  ]
}

hired_employees_avro_schema = {
  "type": "record",
  "name": "HiredEmployee",
  "fields": [
    {"name": "_id", "type": "int"},
    {"name": "datetime", "type": "string"},
    {
      "name": "department",
      "type": ["null", {
        "type": "record",
        "name": "Department",
        "fields": [
          {"name": "_id", "type": "int"},
          {"name": "department", "type": "string", "default": ""}
        ]
      }],
      "default": None
    },
    {
      "name": "job",
      "type": ["null", {
        "type": "record",
        "name": "Job",
        "fields": [
          {"name": "_id", "type": "int"},
          {"name": "job", "type": "string", "default": ""}
        ]
      }],
      "default": None
    }
  ]
}

job_avro_schema = {
  "type": "record",
  "name": "Job",
  "fields": [
    {"name": "_id", "type": "int"},
    {"name": "job", "type": "string", "default": ""}
  ]
}


class AvroWriter:
    def __init__(self, data, schema):
        self.data = data
        self.schema = schema
        self.buffer = io.BytesIO()
        self.s3_client = boto3.client('s3')

    def write_and_dump(self, s3_bucket, s3_key):
        fastavro.writer(self.buffer, self.schema, self.data)
        self.buffer.seek(0)
        self.s3_client.upload_fileobj(self.buffer, s3_bucket, s3_key)


def create_hired_employees_records(employees):
    avro_records = []
    for employee in employees:
        avro_record = {
            '_id': employee._id,
            'datetime': employee.datetime,
            'department': {
                '_id': employee.department._id,
                'department': employee.department.department,
            },
            'job': {
                '_id': employee.job._id,
                'job': employee.job.job,
            },
        }
        avro_records.append(avro_record)

    return avro_records


