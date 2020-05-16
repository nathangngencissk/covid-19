import os
from decimal import Decimal
import uuid

import boto3
import fastparquet

def truncateTable(table):
    #get the table keys
    tableKeyNames = [key.get("AttributeName") for key in table.key_schema]

    """
    NOTE: there are reserved attributes for key names, please see https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ReservedWords.html
    if a hash or range key is in the reserved word list, you will need to use the ExpressionAttributeNames parameter
    described at https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.scan
    """

    #Only retrieve the keys for each item in the table (minimize data transfer)
    ProjectionExpression = ", ".join(tableKeyNames)

    response = table.scan(ProjectionExpression)
    data = response.get('Items')

    while 'LastEvaluatedKey' in response:
        response = table.scan(ProjectionExpression, ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    with table.batch_writer() as batch:
        for each in data:
            batch.delete_item(
                Key={key: each[key] for key in tableKeyNames}
            )

def handle(event, context):    
    s3_bucket = event['Records'][0]['s3']['bucket']['name']
    file_name = "/tmp/latest_report.parquet.gz"
    
    bucket = boto3.resource('s3').Bucket(s3_bucket)
    bucket.download_file(
            Key='latest_report.parquet.gz',
            Filename=file_name
    )
    
    pf = fastparquet.ParquetFile(file_name)
    
    entries = []
    
    for df in pf.iter_row_groups():
        for row in range(pf.count):
            entries.append({
                'id': uuid.uuid4().hex,
                'fips': int(df.iloc[row, 0]),
                'county_US': df.iloc[row, 1],
                'province_state': df.iloc[row, 2],
                'country_region': df.iloc[row, 3],
                'last_update': df.iloc[row, 4],
                'latitude': str(Decimal(str(df.iloc[row, 5]))),
                'longitude': str(Decimal(str(df.iloc[row, 6]))),
                'confirmed': int(df.iloc[row, 7]),
                'deaths': int(df.iloc[row, 8]),
                'recovered': int(df.iloc[row, 9]),
                'active': int(df.iloc[row, 10])
            })
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('covid19')
    
    truncateTable(table)
    
    with table.batch_writer() as batch:
        for item in entries:
            batch.put_item(Item=item)