import requests
import base64
import json
import base64

API_ROOT = 'https://1tn5vi9uuh.execute-api.eu-central-1.amazonaws.com/prod'


def get_image_list(username, bucket_type):
    """
    Returns a list of images in the specified bucket
    Args:
        username (str): The username to list images from
        bucket_type (str): The bucket type to list images from
    Returns:
        list: A list of image names
    """

    payload = {
    "username": username,
    "bucket_type": bucket_type
        }
    response = requests.get(API_ROOT + f'/user/{username}/images', json=payload)

    if response.status_code == 200:
        
        response_json = response.json()

        return eval(response_json['body'])
    else:
        return response.status_code
    

def get_user_history(username):
    """
    Returns user history, saved in dynamoDB table
    Args:
        username (str): The username to get history from
    Returns:
        dict: user history
    """

    payload = {
                "user_login": username
               }
    try:
        response = requests.get(API_ROOT + f'/user/{username}/history', json=payload)
    except:
        return {}

    if response.status_code == 200:
        
        response_json = response.json()

        history = eval(response_json['body'])
        return history
    else:
        return {}
    

def add_watermark(main_image_bytes, watermark_image_bytes, X, Y):
    """
    Adds a watermark to an image
    Args:
        main_image_bytes (bytes): The main image as bytes
        watermark_image_bytes (bytes): The watermark image as bytes
        X (int): The X coordinate of the watermark
        Y (int): The Y coordinate of the watermark
    Returns:
        bytes: The resulting image as bytes
    """

    payload = {
        'main_image': base64.b64encode(main_image_bytes).decode('utf-8'),
        'watermark_image': base64.b64encode(watermark_image_bytes).decode('utf-8'),
        'X': X,
        'Y': Y
    }

    payload_json = json.dumps(payload)

    try:
        response = requests.post(API_ROOT + '/images/watermark', data=payload_json)
    except:
        return False

    if response.status_code == 200:

        response_json = response.json()
        response_body = eval(response_json['body'])['result_image']
        result_image_bytes = base64.b64decode(response_body)

        return result_image_bytes
    
    else:
        return False


def upload_image(image_data, image_name, bucket_type, username):
    """
    Uploads an image to the specified bucket
    Args:
        image_data (bytes): The image as bytes
        image_name (str): The image name
        bucket_type (str): The bucket type to upload to
        username (str): The username to upload to
    Returns:
        dict: The response from the API
    """

    endpoint = API_ROOT + f'/user/{username}/{bucket_type}/images'
    
    payload = {
        'body': base64.b64encode(image_data).decode('utf-8'),
        'name': image_name,
        'bucket_type': bucket_type,
        'username': username
    }

    try:
        response = requests.post(endpoint, json=payload)
        
        if response.status_code == 200:
            return response.json()
        
        else:
            print(f'Failed to upload image. Status code: {response.status_code}. Response: {response.text}')
    
    except requests.exceptions.RequestException as e:
        print('Error connecting to the API:', e)

