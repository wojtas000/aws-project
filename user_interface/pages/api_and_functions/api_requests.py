import requests


LIST_IMAGES_ENDPOINT = "https://1tn5vi9uuh.execute-api.eu-central-1.amazonaws.com/prod/list-images"
USER_HISTORY_ENDPOINT = "https://1tn5vi9uuh.execute-api.eu-central-1.amazonaws.com/prod/user-history"


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