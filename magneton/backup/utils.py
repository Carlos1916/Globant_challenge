
department_avro_schema = {
  "type": "record",
  "name": "Department",
  "fields": [
    {"name": "id", "type": "int"},
    {"name": "department", "type": "string", "default": ""}
  ]
}

hired_employees_avro_schema = {
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
          {"name": "id", "type": "int"},
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
    {"name": "id", "type": "int"},
    {"name": "job", "type": "string", "default": ""}
  ]
}

