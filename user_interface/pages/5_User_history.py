import boto3
import pandas as pd
import requests
import streamlit as st

user_history_endpoint = "https://1tn5vi9uuh.execute-api.eu-central-1.amazonaws.com/prod/user-history"

def User_history(username):
    st.title("User history")
    st.write("Here you can see your history of uploading and deleting images and watermarks")
    
    payload = {
        "user_login": username
    }

    response = requests.get(user_history_endpoint, json=payload)

    if response.status_code == 200:
        
        response_json = response.json()

        history = eval(response_json['body'])
        history = pd.DataFrame(history).sort_values(by=['Date'], ascending=True).set_index('Date')
        st.dataframe(history)
    else:
        st.write("Error: Failed to retrieve history.")


if __name__ == "__main__":

    if 'username' not in st.session_state:
        st.session_state['username'] = None
    
    User_history(username=st.session_state['username'])