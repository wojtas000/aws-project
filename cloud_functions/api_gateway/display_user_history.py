import boto3
import json

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    
    """
    This function is called when the user wants to view their history of actions performed on images.
    It returns a JSON string containing the user's history.
    The event contains:
        - user_login: username of the user whose history will be displayed
    """
    
    try: 
        # Get the user_login from the query parameters in the event
        user_login = event['user_login']

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
        
    except Exception as e:
        print('Error getting user history:', e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Failed to get user history'})
        }
