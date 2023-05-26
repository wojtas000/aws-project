import streamlit as st
import boto3
import phonenumbers
from ui import user_page

# Constants
REGION_NAME = 'us-east-1'
USER_POOL_ID = 'us-east-1_frgt78EiF'
APP_CLIENT_ID = '4krct8l10fd5cb2tgshild0ciq'

# Initialize Cognito client and user pool
client = boto3.client('cognito-idp', region_name=REGION_NAME)

def sign_up_page():
    st.title('Sign Up')

    # Input boxes for user information
    username = st.text_input('Username')
    email = st.text_input('Email')
    phone_number = st.text_input('Phone Number', placeholder='Optional')

    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        phone_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
    
    except phonenumbers.NumberParseException:
        st.error('Invalid phone number')
    
    # Input boxes for password
    password = st.text_input('Password', type='password')
    confirm_password = st.text_input('Confirm Password', type='password')

    # Sign up button
    if st.button('Sign Up'):
        if password == confirm_password:
            try:
                response = client.sign_up(
                    ClientId=APP_CLIENT_ID,
                    Username=username,
                    Password=password,
                    UserAttributes=[
                        {
                            'Name': 'email',
                            'Value': email
                        },
                        {
                            'Name': 'phone_number',
                            'Value': phone_number
                        }
                    ]
                )
                st.success('Sign up successful! Please check your email for a verification link.')
                verification_code = st.text_input('Verification Code')

            except client.exceptions.UsernameExistsException:
                st.error('User already exists')
            except Exception as e:
                st.error(f'Sign up error: {str(e)}')
        else:
            st.error('Passwords do not match')

def sign_in_page():
    st.title('Sign In')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if st.button('Sign In'):
        try:
            response = client.initiate_auth(
                ClientId=APP_CLIENT_ID,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': username,
                    'PASSWORD': password
                }
            )
            # Successful authentication
            access_token = response['AuthenticationResult']['AccessToken']
            st.success('Sign in successful!')
            
            user_page()

        except client.exceptions.NotAuthorizedException:
            st.error('Invalid username or password')
        except client.exceptions.UserNotFoundException:
            st.error('User does not exist')
        except Exception as e:
            st.error(f'Sign in error: {str(e)}')


def main():
    st.sidebar.title('Authentication')
    option = st.sidebar.selectbox('Select Option', ('Sign Up', 'Sign In'))

    if option == 'Sign Up':
        sign_up_page()
    elif option == 'Sign In':
        sign_in_page()


if __name__ == '__main__':
    main()
