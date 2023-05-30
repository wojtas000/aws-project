import requests
import base64

LIST_IMAGES_ENDPOINT = "https://1tn5vi9uuh.execute-api.eu-central-1.amazonaws.com/prod/list-images"
USER_HISTORY_ENDPOINT = "https://1tn5vi9uuh.execute-api.eu-central-1.amazonaws.com/prod/user-history"
INSERT_WATERMARK_ENDPOINT = "https://1tn5vi9uuh.execute-api.eu-central-1.amazonaws.com/prod/add-watermark"

def get_image_list(username, bucket_type):
    payload = {
    "username": username,
    "bucket_type": bucket_type
        }
    response = requests.get(LIST_IMAGES_ENDPOINT, json=payload)

    if response.status_code == 200:
        
        response_json = response.json()

        return eval(response_json['body'])
    else:
        return []
    

def get_user_history(username):
    payload = {
                "user_login": username
               }

    response = requests.get(USER_HISTORY_ENDPOINT, json=payload)

    if response.status_code == 200:
        
        response_json = response.json()

        history = eval(response_json['body'])
        return history
    else:
        return {}
    

import requests
import json

# Define the input parameters for the Lambda function
import base64

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
    response = requests.post(INSERT_WATERMARK_ENDPOINT, data=payload_json)

    # Check the response status code
    if response.status_code == 200:
        response_json = response.json()
        response_body = response_json['body'][17:-1]
        # result_image_base64 = response_body[9:]
        result_image_bytes = base64.b64decode(response_body)
        return result_image_bytes
    
    else:
        return response.status_code
