import io

import boto3
import fastavro
from botocore.exceptions import ClientError

from core.models import Job, Department, HiredEmployee


def parse_s3_uri(s3_uri):
    if not s3_uri.startswith('s3://'):
        raise ValueError("Invalid S3 URI. It should start with 's3://'")

    s3_path = s3_uri[5:]  # Remove 's3://' from the URI
    bucket, key = s3_path.split('/', 1)  # Split by the first occurrence of '/'

    return bucket, key


def insert_data_from_avro(s3_bucket, s3_key):
    s3_client = boto3.client('s3')

    # Download the Avro file from S3
    response = s3_client.get_object(Bucket=s3_bucket, Key=s3_key)
    avro_data = response['Body'].read()

    # Create an Avro reader
    avro_data = list(fastavro.reader(io.BytesIO(avro_data)))

    for r in avro_data:
        print(r)


