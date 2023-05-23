import json
import uuid
import boto3
from datetime import datetime


def lambda_handler(event, context):
    # Retrieve S3 bucket and object information from the event
    s3_bucket = event['Records'][0]['s3']['bucket']['name']
    s3_key = event['Records'][0]['s3']['object']['key']

    # Delete record from DynamoDB table
    dynamodb_client = boto3.client('dynamodb')
    dynamodb_table = 'Images'
    user_history_table = 'User_history'

    item_id = s3_key  # Assuming the Image_ID in DynamoDB matches the S3 object key

    # Delete record from Images table
    dynamodb_client.delete_item(
        TableName=dynamodb_table,
        Key={
            'Image_ID': {'S': item_id}
        }
    )


    # Generate a unique ID using UUID
    unique_id = str(uuid.uuid4())
    
    # Get the current timestamp
    timestamp = datetime.now().isoformat()
    
    action = 'deletion'
    
    item = {
        'ID': {'S': unique_id},
        'Image_ID': {'S': str(s3_key)},
        'Action': {'S': action},
        'Date': {'S': timestamp}
    }
    
    dynamodb_client.put_item(
    TableName=user_history_table,
    Item=item
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Record deleted from DynamoDB and User_history updated')
    }
