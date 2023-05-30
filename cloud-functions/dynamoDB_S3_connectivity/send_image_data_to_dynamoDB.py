import json
import uuid
import boto3
from datetime import datetime

def lambda_handler(event, context):

    s3_client = boto3.client('s3')

    # Retrieve S3 bucket and object information from the event
    s3_bucket = event['Records'][0]['s3']['bucket']['name']
    s3_key = event['Records'][0]['s3']['object']['key']

    # Extract the metadata of the image
    response = s3_client.head_object(Bucket=s3_bucket, Key=s3_key)
    image_size = response['ContentLength']
    image_format = response['ContentType']
    
    # Extract image label using Amazon Rekognition
    rekognition_client = boto3.client('rekognition')
    rekognition_response = rekognition_client.detect_labels(
        Image={'S3Object': {'Bucket': s3_bucket, 'Name': s3_key}},
        MaxLabels=1
    )

    label = rekognition_response['Labels'][0]['Name']
    
    # Update DynamoDB table with image information
    dynamodb_client = boto3.client('dynamodb')
    images_table = 'Images'
    user_history_table = 'User_history'
    

    item = {
        'Image_ID': {'S': str(s3_key)},
        'Label': {'S': label},
        'Size': {'S': str(image_size)},
        'Format': {'S': image_format}
    }
    
    dynamodb_client.put_item(
        TableName=images_table,
        Item=item
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
    
    action = 'upload'
    
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
        'body': json.dumps('Image information updated in DynamoDB and User_history updated')
    }
