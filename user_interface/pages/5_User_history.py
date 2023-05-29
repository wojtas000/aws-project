import boto3
import pandas as pd
import streamlit as st

def return_user_history(user_login):
    # Create a DynamoDB client
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
        activities = pd.DataFrame(columns=['User', 'Action', 'Date'])
        for item in items:
            try:
                if item['User'] == user_login:
                    image_name = item['Image_ID'].split('/')[-1]
                    activities = activities.append({'User': item['User'], 'Date': item['Date'],  'Action': item['Action'] + ' ' + image_name}, ignore_index=True)
                    returned = True
            except:
                pass
        if returned == False:
            print("No items found with user-id '%s'" % user_login)
        else:
            return activities.sort_values(by=['Date'], ascending=True).set_index('Date')
    
if __name__ == "__main__":
    try:
        st.dataframe(return_user_history(st.session_state['username']))
    except:
        st.write('Please sign in to see your history')