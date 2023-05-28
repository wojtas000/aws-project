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


def add_watermark(main_image, watermark_image, X, Y):
    # Open the main image
    # main_image = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    image_width, image_height = main_image.size

    # Open the watermark image
    # watermark_image = Image.open(io.BytesIO(watermark_bytes)).convert("RGBA")
    watermark_width, watermark_height = watermark_image.size

    # Resize the watermark image to fit within the main image
    if watermark_width > image_width or watermark_height > image_height:
        watermark_image.thumbnail((image_width, image_height), Image.ANTIALIAS)

    # Calculate the position to place the watermark
    pos_x = int((image_width - watermark_image.size[0]) * X / 10)
    pos_y = int((image_height - watermark_image.size[1]) * (10 - Y) / 10)

    # Apply the watermark onto the main image
    main_image.paste(watermark_image, (pos_x, pos_y), mask=watermark_image)

    return main_image


def remove_watermark(image_bytes):
    # Load the image
    image = Image.open(io.BytesIO(image_bytes)).convert("RGBA")

    # TODO: Implement watermark removal logic here
    # Replace the code below with your watermark removal algorithm

    # Simply return the original image for now
    return image



def apply_watermark_page(username):
    if st.session_state['username'] is None:
        st.write('You have to sign in first!')
        st.stop()
    else:
        username = st.session_state['username']
        st.title("Apply Watermark")
     
        image, watermark = st.columns(2)

        with image:

            images = list_images(username)

            if images==[]:
                st.write("You don't have any images yet")

            chosen_image_name = st.selectbox("Select image", images)


        with watermark:

            watermarks = list_watermarks(username)
            if watermarks==[]:
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

        # File uploader for the image with watermark
        image_file = st.file_uploader("Upload the image with watermark", type=["png", "jpg", "jpeg"])

        if image_file:
            # Display the uploaded image
            st.image(image_file, caption="Image with Watermark", use_column_width=True)

            # Button to remove watermark
            if st.button("Remove Watermark"):
                # Convert file uploader object to bytes
                image_bytes = image_file.read()

                # Remove the watermark from the image
                result_image = remove_watermark(image_bytes)

                # Display the resulting image
                st.image(result_image, caption="Result", use_column_width=True)


if __name__=='__main__':
    if 'username' not in st.session_state:
        st.session_state['username'] = None
    apply_watermark_page(username=st.session_state['username'])