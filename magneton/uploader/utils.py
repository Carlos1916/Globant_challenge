import re
import datetime
import logging


import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_upload_path(instance, filename):
    folder = 'uploads/raw/'
    filename = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
    return f"{folder}{instance.file_type}/{instance.file_table}/{filename}"


def is_positive_integer(value):
    try:
        return int(value) > 0
    except ValueError:
        return False


def is_iso_datetime(value):
    # Example: 2020-01-01T00:00:00Z
    if pd.notna(value):
        is_datetime_regex = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$'
        return re.match(is_datetime_regex, value) is not None
    else:
        return False


def validate_row_hired_employees(row):
    is_valid_id = is_positive_integer(row['id'])
    is_valid_datetime = is_iso_datetime(row['datetime'])
    is_valid_department_id = is_positive_integer(row['department_id'])
    is_valid_product_id = is_positive_integer(row['job_id'])

    return is_valid_id and is_valid_datetime and is_valid_department_id and is_valid_product_id


def validate_row_departments(row):
    is_valid_id = is_positive_integer(row['id'])

    return is_valid_id


def validate_row_jobs(row):
    is_valid_id = is_positive_integer(row['id'])
    return is_valid_id


def clean_csv(csv_file, schema, instance):

    df = pd.read_csv(csv_file, names=schema.keys())

    logger.info(f"Dataframe head: {df.head()}")
    valid_rows = []
    invalid_rows = []

    validation_function = globals()[f"validate_row_{instance.file_table}"]
    logger.info(f"Validation function: {validation_function.__name__}")
    for index, row in df.iterrows():
        if validation_function(row):
            valid_rows.append(df.iloc[index])
        else:
            invalid_rows.append(df.iloc[index])

    valid_df = pd.DataFrame(valid_rows)

    if invalid_rows:
        logging.info(f"Invalid rows:")
        for row in invalid_rows:
            logging.info(f"{row}")

    logger.info(f"Valid rows: {len(valid_df)}")
    logger.info(f"Invalid rows: {len(invalid_rows)}")

    # valid_df = valid_df.astype(schema)
    return valid_df


def build_clean_path(instance, filename):
    folder = 'uploads/clean/'
    return f"{folder}{instance.file_type}/{instance.file_table}/{filename}"


def assign_schema(instance):

    schemas = {
        'jobs': {
            'id': int,
            'job': str
            },
        'hired_employees': {
            'id': int,
            'name': str,
            'datetime': str,
            'department_id': int,
            'job_id': int
            },
        'departments': {
            'id': int,
            'department': str
            }
    }

    return schemas.get(instance.file_table, None)


