import os

import boto3
import requests
from datetime import date, timedelta, datetime
import papermill as pm


def handle(event, context):
    pm.execute_notebook(
        'covid-19.ipynb',
        '/tmp/output.ipynb'
    )

    s3_bucket = os.environ['s3_bucket']
    bucket = boto3.resource('s3').Bucket(s3_bucket)
    bucket.upload_file(
        Key='latest_report.parquet.gz',
        Filename='/tmp/latest_report.parquet.gz'
    )