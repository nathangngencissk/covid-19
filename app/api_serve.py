import json
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Key, Attr

def default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)

def handle(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('covid19')
    
    response = table.scan(
        FilterExpression=Attr('confirmed').ne('0')
    )
    
    items = response['Items']
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            'items': items
        }, default=default)
    }