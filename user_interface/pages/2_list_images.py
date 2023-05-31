import streamlit as st
import boto3
from pages.api_and_functions.api_requests import get_image_list

# Create S3 client
s3 = boto3.client('s3')


def list_images_page(username):
    
    if st.session_state['username'] is None:
        st.write('You have to sign in first!')
        st.stop()
    
    else:
        st.title("View your images and watermarks")
        
        image, watermark = st.columns(2)
        

        with image:
            st.write("Your images:")
            
            images = get_image_list(username, 'images')

            if images:
                for i, obj in enumerate(images):
                    if len(obj) > 25:
                        obj = obj[:25] + '...'
                    st.write(f"{i+1}. {obj}")
            else:
                st.write("No images found.")

            if st.button('Delete all images'):
                for image in images:
                    s3.delete_object(Bucket='watermark-project-images-bucket', Key=image)
        

        with watermark:
            st.write("Your watermarks:")
            
            watermarks = get_image_list(username, 'watermarks')
            
            if watermarks:
                for i, obj in enumerate(watermarks):
                    if len(obj) > 25:
                        obj = obj[:25] + '...'
                    st.write(f"{i+1}. {obj}")
            else:
                st.write("No watermarks found.")
     
            if st.button('Delete all watermarks'):
                for watermark in watermarks:
                    s3.delete_object(Bucket='watermark-project-watermarks-bucket', Key=watermark)


if __name__=='__main__':
    
    if 'username' not in st.session_state:
        st.session_state['username'] = None

    list_images_page(username=st.session_state['username'])