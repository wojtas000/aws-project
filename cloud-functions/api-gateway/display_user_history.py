import boto3
import json

def lambda_handler(event, context):
    # Get the user_login from the query parameters in the event
    user_login = event['user_login']

    dynamodb = boto3.resource('dynamodb')

    # Specify the table name
    table_name = 'User_history'

    # Get the DynamoDB table
    table = dynamodb.Table(table_name)

    # Scan the table to retrieve all items
    response = table.scan()

    # Check if any items were returned
    if 'Items' in response:
        items = response['Items']
        returned = False
        activities = {'User': [], 'Action': [], 'Date': []}
        for item in items:
            try:
                if item['User'] == user_login:
                    image_name = item['Image_ID'].split('/')[-1]
                    activities['User'].append(item['User'])
                    activities['Date'].append(item['Date'])
                    activities['Action'].append(item['Action'] + ' ' + image_name)
                    returned = True
            except:
                pass
        if returned == False:
            # Return an empty response with status code 200
            return {
                'statusCode': 200,
                'body': ''
            }
        else:
            activities_json = json.dumps(activities)
            

            # Return the activities JSON string with status code 200
            return {
                'statusCode': 200,
                'body': activities_json
            }
    else:
        # Return an empty response with status code 200
        return {
            'statusCode': 200,
            'body': ''
        }
