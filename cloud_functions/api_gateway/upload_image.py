import json
import boto3
import base64


s3 = boto3.client('s3', region_name='eu-central-1')

def lambda_handler(event, context):

    """
    This function is called when the user wants to upload an image or watermark to S3.
    It returns a JSON string containing a message indicating whether the upload was successful.
    The event contains:
        - body: base64-encoded image data
        - name: name of the image
        - bucket_type: type of bucket (images or watermarks)
        - username: username of the user who owns the image
    """

    try:
        # Extract image data from the request
        image_data = event['body']
        image_name = event['name']
        bucket_type = event['bucket_type']
        username = event['username']
        
        # Decode the base64 image data
        decoded_image = base64.b64decode(image_data)
        bucket_name = f'watermark-project-{bucket_type}-bucket'
        # Upload the image to S3
        s3.put_object(Body=decoded_image, Bucket=bucket_name, Key=username+'/'+image_name)
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Image uploaded successfully'})
        }
    
    except Exception as e:
        print('Error uploading image:', e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Failed to upload image'})
        }
