import requests
import base64
import json
import base64
import io

API_ROOT = 'https://1tn5vi9uuh.execute-api.eu-central-1.amazonaws.com/prod'

LIST_IMAGES_ENDPOINT = "https://1tn5vi9uuh.execute-api.eu-central-1.amazonaws.com/prod/list-images"
USER_HISTORY_ENDPOINT = "https://1tn5vi9uuh.execute-api.eu-central-1.amazonaws.com/prod/user-history"
INSERT_WATERMARK_ENDPOINT = "https://1tn5vi9uuh.execute-api.eu-central-1.amazonaws.com/prod/add-watermark"


def get_image_list(username, bucket_type):
    params = {
    "username": username,
    "bucket_type": bucket_type
        }
    response = requests.get(API_ROOT + f'/user/{username}/images', json=params)

    if response.status_code == 200:
        
        response_json = response.json()

        return eval(response_json['body'])
    else:
        return response.status_code
    

def get_user_history(username):
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
    payload = {
        'main_image': base64.b64encode(main_image_bytes).decode('utf-8'),
        'watermark_image': base64.b64encode(watermark_image_bytes).decode('utf-8'),
        'X': X,
        'Y': Y
    }

    # Convert the payload to JSON
    payload_json = json.dumps(payload)

    # Make the POST request to invoke the Lambda function
    try:
        response = requests.post(API_ROOT + '/images/watermark', data=payload_json)
    except:
        return False

    # Check the response status code
    if response.status_code == 200:

        response_json = response.json()
        response_body = eval(response_json['body'])['result_image']
        # result_image_base64 = response_body[9:]
        result_image_bytes = base64.b64decode(response_body)
        return result_image_bytes
    
    else:
        return False


def upload_image(image_data, image_name, bucket_type, username):
    endpoint = API_ROOT + f'/user/{username}/{bucket_type}/images'
    payload = {
        'body': base64.b64encode(image_data).decode('utf-8'),
        'name': image_name,
        'bucket_type': bucket_type,
        'username': username
    }
    print(image_name, bucket_type, username)
    print(endpoint)
    try:
        response = requests.post(endpoint, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Failed to upload image. Status code: {response.status_code}. Response: {response.text}')
    except requests.exceptions.RequestException as e:
        print('Error connecting to the API:', e)

