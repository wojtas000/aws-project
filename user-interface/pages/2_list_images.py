
import streamlit as st
import boto3

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

def list_images_page(username):
    if st.session_state['username'] is None:
        st.write('You have to sign in first!')
        st.stop()
    else:
        st.title("View your images and watermarks")
        image, watermark = st.columns(2)
        with image:
            st.write("Your images:")
            images = list_images(username)
            if images==[]:
                st.write("You don't have any images yet")

            chosen_image_name = st.selectbox("Select image", images)

            if st.button('Delete all images'):
                for image in images:
                    s3.delete_object(Bucket='watermark-project-images-bucket', Key=image)
        
        with watermark:
            st.write("Your watermarks:")
            watermarks = list_watermarks(username)
            if watermarks==[]:
                st.write("You don't have any watermarks yet")

            chosen_image_name = st.selectbox("Select watermark", images)

            if st.button('Delete all watermarks'):
                for watermark in watermarks:
                    s3.delete_object(Bucket='watermark-project-watermarks-bucket', Key=watermark)

list_images_page(username=st.session_state['username'])