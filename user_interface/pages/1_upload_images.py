import streamlit as st
import boto3
from pages.api_package.api_requests import get_image_list

# Create S3 client
s3 = boto3.client('s3')


def upload_page(username):
    
    if st.session_state['username'] is None:
        st.write('You have to sign in first!')
        st.stop()

    else:
        username = st.session_state['username']
        st.title("Upload images and watermarks")
            
        image, watermark = st.columns(2)


        with image:
            
            image_file = st.file_uploader("Upload the main image", type=["png"])
            
            temp_list_of_images = get_image_list(username, 'images')
            
            if image_file and (username+'/'+image_file.name) not  in temp_list_of_images:
                s3.upload_fileobj(image_file, 'watermark-project-images-bucket', username+'/'+image_file.name)

            if st.button("Upload image to database"):
                if image_file and (username+'/'+image_file.name) not  in temp_list_of_images:
                    s3.upload_fileobj(image_file, 'watermark-project-images-bucket', username+'/'+image_file.name)
                    st.experimental_rerun()


        with watermark:
            
            watermark_file = st.file_uploader("Upload the watermark", type=["png"])
            
            temp_list_of_watermarks = get_image_list(username, 'watermarks')

            if st.button("Upload watermark to database"):
                if watermark_file and (username+'/'+watermark_file.name) not in temp_list_of_watermarks:
                    s3.upload_fileobj(watermark_file, 'watermark-project-watermarks-bucket', username+'/'+watermark_file.name)
                    st.experimental_rerun()


if __name__=='__main__':
    if 'username' not in st.session_state:
        st.session_state['username'] = None
    upload_page(username=st.session_state['username'])