import streamlit as st
from PIL import Image
import io
import boto3
from pages.api_package.api_requests import get_image_list
from pages.api_package.add_remove_watermark import add_watermark

# Create S3 client
s3 = boto3.client('s3')


def apply_watermark_page(username):
    
    if st.session_state['username'] is None:
        st.write('You have to sign in first!')
        st.stop()
    
    else:
        username = st.session_state['username']
        st.title("Apply Watermark")
     
        image, watermark = st.columns(2)


        with image:

            images = get_image_list(username, 'images')

            if not images:
                st.write("You don't have any images yet")

            chosen_image_name = st.selectbox("Select image", images)


        with watermark:

            watermarks = get_image_list(username, 'watermarks')

            if not watermarks:
                st.write("You don't have any watermarks yet")
        
            chosen_watermark_name = st.selectbox("Select watermark", watermarks)
        

        # download choosen image
        image_file = s3.get_object(Bucket='watermark-project-images-bucket', Key=chosen_image_name)
        image_file = image_file['Body'].read()
        image_file = Image.open(io.BytesIO(image_file)).convert("RGBA")

        # download choosen watermark
        watermark_file = s3.get_object(Bucket='watermark-project-watermarks-bucket', Key=chosen_watermark_name)
        watermark_file = watermark_file['Body'].read()
        watermark_file = Image.open(io.BytesIO(watermark_file)).convert("RGBA")

        if image_file and watermark_file:
            col1, col2 = st.columns(2)
            # Display the uploaded main image
            with col1:    
                st.image(image_file, caption="Main Image", use_column_width=True)
            # Display the uploaded watermark image
            with col2:
                st.image(watermark_file, caption="Watermark", use_column_width=True)

            st.write("Choose the position of the watermark:")
            st.write("X: 0 - left, 10 - right")
            st.write("Y: 0 - bottom, 10 - top")
            X = st.slider('X', 0, 10, 1)
            Y = st.slider('Y', 0, 10, 1)

            # Button to add watermark
            if st.button("Add Watermark"):
                
                # Convert file uploader objects to bytes
                image_bytes = image_file
                watermark_bytes = watermark_file

                # # Add watermark to the main image
                result_image = add_watermark(image_bytes, watermark_bytes, X, Y)

                # # Display the resulting image
                st.image(result_image, caption="Result", use_column_width=True)


if __name__=='__main__':
    if 'username' not in st.session_state:
        st.session_state['username'] = None
    apply_watermark_page(username=st.session_state['username'])