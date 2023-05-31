import streamlit as st
import boto3
from pages.api_and_functions.api_requests import get_image_list, upload_image

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
            if image_file:
                st.image(image_file, caption=image_file.name, use_column_width=True)

            temp_list_of_images = get_image_list(username, 'images')
            

            if st.button("Upload image to database"):
                if image_file and (username+'/'+image_file.name) not  in temp_list_of_images:
                    
                    response = upload_image(image_data=image_file.read(), 
                                            image_name=image_file.name, 
                                            bucket_type='images', 
                                            username=username)
        
                    st.experimental_rerun()


        with watermark:
            
            watermark_file = st.file_uploader("Upload the watermark", type=["png"])
            if watermark_file:
                st.image(watermark_file, caption=watermark_file.name, use_column_width=True)
            temp_list_of_watermarks = get_image_list(username, 'watermarks')

            if st.button("Upload watermark to database"):
                if watermark_file and (username+'/'+watermark_file.name) not in temp_list_of_watermarks:
                    
                    response = upload_image(image_data=watermark_file.read(), 
                        image_name=watermark_file.name, 
                        bucket_type='watermarks', 
                        username=username)
            
                    st.experimental_rerun()


if __name__=='__main__':
    if 'username' not in st.session_state:
        st.session_state['username'] = None
    upload_page(username=st.session_state['username'])