import json
import boto3

def lambda_handler(event, context):
    # Extract the username from the event payload
    username = event['username']
    bucket_type = event['bucket_type']

    # Create an S3 client
    s3 = boto3.client('s3')
    
    if bucket_type == 'images':
        response = s3.list_objects(Bucket='watermark-project-images-bucket', Prefix=username+'/')
    elif bucket_type == 'watermarks':
        response = s3.list_objects(Bucket='watermark-project-watermarks-bucket', Prefix=username+'/')
    objects = []

    if 'Contents' in response:
        for obj in response['Contents']:
            objects.append(obj['Key'])

    # Return the list of image objects
    return {
        'statusCode': 200,
        'body': json.dumps(objects)
    }
