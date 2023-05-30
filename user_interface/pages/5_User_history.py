import pandas as pd
import streamlit as st
from pages.api_package.api_requests import get_user_history


def User_history(username):
    
    st.title("User history")
    st.write("Here you can see your history of uploading and deleting images and watermarks")
    
    history = get_user_history(username)

    if history:
        history = pd.DataFrame(history).sort_values(by=['Date'], ascending=True).set_index('Date')
        st.dataframe(history)

    else:
        st.write("Error: Failed to retrieve history.")


if __name__ == "__main__":

    if 'username' not in st.session_state:
        st.session_state['username'] = None
    
    User_history(username=st.session_state['username'])

