import json
import boto3


s3 = boto3.client('s3', region_name='eu-central-1')

def lambda_handler(event, context):

    """
    This function is called when the user wants to view list of images or watermarks.
    It returns a JSON string containing the list of images or watermarks.
    The event contains:
        - username: username of the user whose images or watermarks will be listed
        - bucket_type: type of bucket (images or watermarks)
    """
    
    try:
        # Extract the username from the event payload
        username = event['username']
        bucket_type = event['bucket_type']
        
        # List all objects in the bucket
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
    
    except Exception as e:
        print('Error listing objects:', e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Failed to list objects'})
        }