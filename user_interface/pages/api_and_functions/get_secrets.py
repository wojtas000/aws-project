import boto3
from botocore.exceptions import ClientError
import json

def get_cognito_secrets():
    """
    Get Cognito secrets from AWS Secrets Manager
    """

    secret_name = "Cognito_secrets"
    region_name = "eu-central-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )

        secret_string = get_secret_value_response['SecretString']
        secret_dict = json.loads(secret_string)

        user_pool_id = secret_dict['USER_POOL_ID']
        app_client_id = secret_dict['APP_CLIENT_ID']

        return user_pool_id, app_client_id

    except ClientError as e:
        raise e