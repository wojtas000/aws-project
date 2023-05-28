from io import BytesIO
import streamlit as st
from PIL import Image
import io
import boto3
import json
from botocore.exceptions import ClientError



# # Tworzenie sesji

# aws_access_key_id, aws_secret_access_key = get_secrets()

# session = boto3.Session(
#     aws_access_key_id=aws_access_key_id,
#     aws_secret_access_key=aws_secret_access_key
# )

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

# aws_region = 'us-east-1'  # Replace with your desired region

# # Create an S3 client
# s3 = boto3.client('s3', region_name=aws_region)

# # Replace 'your-lambda-function-name' with your actual Lambda function name
# lambda_function_name = 'upload_photo_to_the_bucket'

# # Streamlit app code
# def uploader():
#     st.title("Photo Uploader")
    
#     # File uploader
#     photo = st.file_uploader("Upload a photo", type=['jpg', 'jpeg', 'png'])
    
#     if photo is not None:
#         st.image(photo, caption='Uploaded photo', use_column_width=True)
    
#         # Invoke the Lambda function
#         invoke_lambda(photo)
#         st.success('Photo uploaded successfully')

# def invoke_lambda(photo):
#     # Convert the photo to bytes
#     photo_bytes = photo.read()
    
#     # Invoke the Lambda function
#     lambda_client = boto3.client('lambda', region_name=aws_region)
#     lambda_client.invoke(
#         FunctionName=lambda_function_name,
#         InvocationType='Event',
#         Payload=photo_bytes
#     )

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


# Streamlit app code
def user_page(username):
    st.title("Watermark App")
    st.write("Choose an option:")

    option = st.radio("Select an option", ("Add Watermark", "Remove Watermark"))

    if option == "Add Watermark":
        
        image, watermark = st.columns(2)

        with image:
            # File uploader for the main image
            image_file = st.file_uploader("Upload the main image", type=["png"])
            if image_file:
                s3.upload_fileobj(image_file, 'watermark-project-images-bucket', username+'/'+image_file.name)

            if st.button("Upload image to database"):
                st.experimental_rerun()

            st.write("Your images:")
            images = list_images(username)

            if images==[]:
                st.write("You don't have any images yet")
                return

            chosen_image_name = st.selectbox("Select image", images)

            if st.button('Delete all images'):
                for image in images:
                    s3.delete_object(Bucket='watermark-project-images-bucket', Key=image)


        with watermark:
            # # File uploader for the watermark
            watermark_file = st.file_uploader("Upload the watermark", type=["png"])
            if watermark_file:
                s3.upload_fileobj(watermark_file, 'watermark-project-watermarks-bucket', username+'/'+watermark_file.name)

            if st.button("Upload watermark to database"):
                st.experimental_rerun()

            st.write("Your watermarks:")
            watermarks = list_watermarks(username)
            if watermarks==[]:
                st.write("You don't have any watermarks yet")
                return
        
            chosen_watermark_name = st.selectbox("Select watermark", watermarks)

            if st.button('Delete all watermarks'):
                for watermark in watermarks:
                    s3.delete_object(Bucket='watermark-project-watermarks-bucket', Key=watermark)
        
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

    elif option == "Remove Watermark":
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


# Run the Streamlit app
if __name__ == "__main__":
    user_page(username=st.session_state['username'])