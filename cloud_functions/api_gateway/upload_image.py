import json
import boto3
import base64

s3 = boto3.client('s3', region_name='eu-central-1')

def lambda_handler(event, context):
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
