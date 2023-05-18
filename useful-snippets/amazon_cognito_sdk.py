import boto3

# Configure the Cognito client
client = boto3.client('cognito-idp', region_name='your_region')

# User Pool ID and App Client ID
user_pool_id = 'your_user_pool_id'
app_client_id = 'your_app_client_id'

def register_user(username, password, email):
    try:
        response = client.sign_up(
            ClientId=app_client_id,
            Username=username,
            Password=password,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': email
                }
            ]
        )
        print('User registered successfully!')
        print('Confirmation code:', response['UserConfirmed'])
    except Exception as e:
        print('Error registering user:', str(e))

def confirm_registration(username, confirmation_code):
    try:
        response = client.confirm_sign_up(
            ClientId=app_client_id,
            Username=username,
            ConfirmationCode=confirmation_code
        )
        print('User registration confirmed!')
    except Exception as e:
        print('Error confirming user registration:', str(e))

def sign_in_user(username, password):
    try:
        response = client.initiate_auth(
            ClientId=app_client_id,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )
        access_token = response['AuthenticationResult']['AccessToken']
        print('User signed in successfully!')
        print('Access Token:', access_token)
    except Exception as e:
        print('Error signing in user:', str(e))

# Example usage
register_user('username', 'password123', 'user@example.com')
confirm_registration('username', '123456')
sign_in_user('username', 'password123')
