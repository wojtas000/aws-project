from io import BytesIO
import streamlit as st
from PIL import Image
import io
import boto3
import requests
import json
from botocore.exceptions import ClientError


# Tworzenie klienta S3
s3 = boto3.client('s3')

list_images_endpoint = "https://1tn5vi9uuh.execute-api.eu-central-1.amazonaws.com/prod/list-images"
put_image_endpoint = "https://1tn5vi9uuh.execute-api.eu-central-1.amazonaws.com/prod"



def upload_page(username):
    if st.session_state['username'] is None:
        st.write('You have to sign in first!')
        st.stop()
    else:
        username = st.session_state['username']
        st.title("Upload images and watermarks")
            
        image, watermark = st.columns(2)

        with image:
            # File uploader for the main image
            image_file = st.file_uploader("Upload the main image", type=["png"])
            
            payload = {
                "username": username,
                "bucket_type": "images"
                }
            response = requests.get(list_images_endpoint, json=payload)
            
            if response.status_code == 200:
                # Parse the response JSON
                response_json = response.json()

                # Extract the body from the response
                temp_list_of_images = eval(response_json['body'])
            else:
                temp_list_of_images = []
            
            if image_file and (username+'/'+image_file.name) not  in temp_list_of_images:
                s3.upload_fileobj(image_file, 'watermark-project-images-bucket', username+'/'+image_file.name)

            if st.button("Upload image to database"):
                st.experimental_rerun()


        with watermark:
            # # File uploader for the watermark
            watermark_file = st.file_uploader("Upload the watermark", type=["png"])
            
            payload = {
                "username": username,
                "bucket_type": "watermarks"
            }
            response = requests.get(list_images_endpoint, json=payload)
            
            if response.status_code == 200:
                # Parse the response JSON
                response_json = response.json()

                # Extract the body from the response
                temp_list_of_watermarks = eval(response_json['body'])
            else:
                temp_list_of_watermarks = []

            if watermark_file and (username+'/'+watermark_file.name) not in temp_list_of_watermarks:
                s3.upload_fileobj(watermark_file, 'watermark-project-watermarks-bucket', username+'/'+watermark_file.name)

            if st.button("Upload watermark to database"):
                st.experimental_rerun()


if __name__=='__main__':
    if 'username' not in st.session_state:
        st.session_state['username'] = None
    upload_page(username=st.session_state['username'])