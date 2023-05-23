import json
import uuid
import boto3

def lambda_handler(event, context):
    # Retrieve S3 bucket and object information from the event
    s3_bucket = event['Records'][0]['s3']['bucket']['name']
    s3_key = event['Records'][0]['s3']['object']['key']

    # Extract image metadata using Amazon Rekognition or any other image analysis library

    # Example: Extract image metadata using Amazon Rekognition
    rekognition_client = boto3.client('rekognition')
    response = rekognition_client.detect_labels(
        Image={'S3Object': {'Bucket': s3_bucket, 'Name': s3_key}},
        MaxLabels=10
    )
    labels = [label['Name'] for label in response['Labels']]
    
    # Update DynamoDB table with image information
    dynamodb_client = boto3.client('dynamodb')
    dynamodb_table = 'Images'
    user_history_table = 'User_history'

    item = {
        'Image_ID': {'S': str(s3_key)},
        'Labels': {'SS': labels}
    }
    
    
    dynamodb_client.put_item(
        TableName=dynamodb_table,
        Item=item
    )
    
    # Generate a unique ID using UUID
    unique_id = str(uuid.uuid4())
    
    action = 'upload'
    
    item = {
        'ID': {'S': unique_id},
        'Image_ID': {'S': str(s3_key)},
        'Action': {'S': action}
    }
    
    dynamodb_client.put_item(
    TableName=user_history_table,
    Item=item
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Image information updated in DynamoDB and User_history updated')
    }
