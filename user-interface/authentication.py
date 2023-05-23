import streamlit as st
import boto3
import phonenumbers

# Constants
REGION_NAME = 'us-east-1'
USER_POOL_ID = 'us-east-1_NoeMtAIEu'
APP_CLIENT_ID = '7a8d9r2nvnee7228m0pmm2n3n5'

# Initialize Cognito client and user pool
client = boto3.client('cognito-idp', region_name=REGION_NAME)

def sign_up_page():
    st.title('Sign Up')
    username = st.text_input('Username')
    email = st.text_input('Email')
    phone_number = st.text_input('Phone Number')

    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        phone_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
    except phonenumbers.NumberParseException:
        st.error('Invalid phone number')
    password = st.text_input('Password', type='password')
    confirm_password = st.text_input('Confirm Password', type='password')

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
                st.success('Sign up successful! Please check your email for a verification code.')
                verification_code = st.text_input('Verification Code')
                if st.button('Verify'):
                    try:
                        response = client.confirm_sign_up(
                            ClientId=APP_CLIENT_ID,
                            Username=email,
                            ConfirmationCode=verification_code
                        )
                        st.success('Verification successful! You can now sign in.')
                    except client.exceptions.UserNotFoundException:
                        st.error('User does not exist')
                    except client.exceptions.CodeMismatchException:
                        st.error('Invalid verification code')
                    except Exception as e:
                        st.error(f'Verification error: {str(e)}')
            except client.exceptions.UsernameExistsException:
                st.error('User already exists')
            except Exception as e:
                st.error(f'Sign up error: {str(e)}')
        else:
            st.error('Passwords do not match')

def sign_in_page():
    st.title('Sign In')
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')

    if st.button('Sign In'):
        try:
            response = client.initiate_auth(
                ClientId=APP_CLIENT_ID,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': email,
                    'PASSWORD': password
                }
            )
            # Successful authentication
            access_token = response['AuthenticationResult']['AccessToken']
            st.success('Sign in successful!')
            user_page(access_token)
        except client.exceptions.NotAuthorizedException:
            st.error('Invalid username or password')
        except client.exceptions.UserNotFoundException:
            st.error('User does not exist')
        except Exception as e:
            st.error(f'Sign in error: {str(e)}')

def user_page(access_token):
    st.title('User Page')
    st.write(f'Access Token: {access_token}')
    # Add your code to display user-specific content or functionality

def main():
    st.sidebar.title('Authentication')
    option = st.sidebar.selectbox('Select Option', ('Sign Up', 'Sign In'))

    if option == 'Sign Up':
        sign_up_page()
    elif option == 'Sign In':
        sign_in_page()

if __name__ == '__main__':
    main()
