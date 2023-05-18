import streamlit as st
import boto3

# Create an AWS Lambda client
lambda_client = boto3.client('lambda')

def invoke_lambda_function1():
    # Invoke Lambda function 1
    response = lambda_client.invoke(
        FunctionName='lambda-function-1',
        InvocationType='Event'  # Invoke asynchronously
    )
    # Process the response if needed

def invoke_lambda_function2():
    # Invoke Lambda function 2
    response = lambda_client.invoke(
        FunctionName='lambda-function-2',
        InvocationType='Event'  # Invoke asynchronously
    )
    # Process the response if needed

# Streamlit app code
st.title("Invoke Lambda Functions")

# Button to invoke Lambda function 1
if st.button("Invoke Lambda Function 1"):
    invoke_lambda_function1()

# Button to invoke Lambda function 2
if st.button("Invoke Lambda Function 2"):
    invoke_lambda_function2()
