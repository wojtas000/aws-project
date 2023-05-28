from io import BytesIO
import streamlit as st
from PIL import Image
import io
import boto3
import json
from botocore.exceptions import ClientError


# Tworzenie klienta S3
s3 = boto3.client('s3')

def list_images(username):
    response = s3.list_objects(Bucket='watermark-project-images-bucket', Prefix=username+'/')
    objects = []
    if 'Contents' in response:
        for obj in response['Contents']:
            objects.append(obj['Key'])
    return objects

def list_watermarks(username):
    response = s3.list_objects(Bucket='watermark-project-watermarks-bucket', Prefix=username+'/')
    objects = []
    if 'Contents' in response:
        for obj in response['Contents']:
            objects.append(obj['Key'])
    return objects


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
            temp_list_of_images = list_images(username)
            if image_file and image_file.name not  in temp_list_of_images:
                s3.upload_fileobj(image_file, 'watermark-project-images-bucket', username+'/'+image_file.name)

            if st.button("Upload image to database"):
                st.experimental_rerun()


        with watermark:
            # # File uploader for the watermark
            watermark_file = st.file_uploader("Upload the watermark", type=["png"])
            temp_list_of_watermarks = list_watermarks(username)
            if watermark_file and watermark_file.name not in temp_list_of_watermarks:
                s3.upload_fileobj(watermark_file, 'watermark-project-watermarks-bucket', username+'/'+watermark_file.name)

            if st.button("Upload watermark to database"):
                st.experimental_rerun()
        


upload_page(username=st.session_state['username'])