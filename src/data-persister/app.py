# src/data-persister/app.py

import json
import os
import boto3
from datetime import datetime

# Get the table name from an environment variable
TABLE_NAME = os.environ['TABLE_NAME']

dynamodb_resource = boto3.resource('dynamodb')
table = dynamodb_resource.Table(TABLE_NAME)

def lambda_handler(event, context):
    """
    Receives data from the Step Function and saves it to DynamoDB.
    """
    print(f"Received event: {json.dumps(event)}")
    
    # Add a timestamp
    timestamp = datetime.utcnow().isoformat()
    
    item_to_save = {
        'id': event['id'],
        'email': event['email'],
        'message': event['message'],
        'sentiment': event['sentiment'],
        'createdAt': timestamp
    }
    
    # Save the item to the DynamoDB table
    table.put_item(Item=item_to_save)
    
    print(f"Successfully saved item to DynamoDB: {item_to_save}")
    
    return item_to_save