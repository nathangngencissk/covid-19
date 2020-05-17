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

    s3_bucket_url = os.environ['s3_bucket']
    website_bucket_url= os.environ['website_bucket']
    
    s3_bucket = boto3.resource('s3').Bucket(s3_bucket_url)
    s3_bucket.upload_file(
        Key='latest_report.parquet.gz',
        Filename='/tmp/latest_report.parquet.gz'
    )
    
    website_bucket = boto3.resource('s3').Bucket(website_bucket_url)
    website_bucket.upload_file(
        Key='latest_report.csv',
        Filename='/tmp/latest_report.csv', 
        ExtraArgs={'ACL':'public-read'}
    )
