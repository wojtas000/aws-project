import json
import uuid
import boto3
from datetime import datetime


dynamodb_client = boto3.client('dynamodb', region_name='eu-central-1')


def lambda_handler(event, context):

    """
    This function is called when the user deletes an image from S3.
    It deletes the record from the DynamoDB Images table and updates the User_history table with appropriate information.
    """

    # Retrieve S3 bucket and object information from the event
    s3_bucket = event['Records'][0]['s3']['bucket']['name']
    s3_key = event['Records'][0]['s3']['object']['key']

    # Specify the table names
    dynamodb_table = 'Images'
    user_history_table = 'User_history'

    # Get the item ID
    item_id = s3_key

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
    
    # Extract the user from the image key if the key is in the correct format
    if '/' in s3_key:
        user = s3_key.split('/')[0]
    else:
        user = 'Unknown'
    
    # Perform the deletion action
    action = 'deletion'
    
    item = {
        'ID': {'S': unique_id},
        'Image_ID': {'S': str(s3_key)},
        'Action': {'S': action},
        'Date': {'S': timestamp},
        'User': {'S': user}
    }
    
    dynamodb_client.put_item(
    TableName=user_history_table,
    Item=item
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Record deleted from DynamoDB and User_history updated')
    }