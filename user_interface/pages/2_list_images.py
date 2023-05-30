
import streamlit as st
import boto3
import requests
import json

s3 = boto3.client('s3')

api_url = "https://1tn5vi9uuh.execute-api.eu-central-1.amazonaws.com/prod/list-images"

def list_images_page(username):
    if st.session_state['username'] is None:
        st.write('You have to sign in first!')
        st.stop()
    else:
        st.title("View your images and watermarks")
        image, watermark = st.columns(2)
        with image:
            st.write("Your images:")
            payload = {
                            "username": username,
                            "bucket_type": "images"
                        }
            response = requests.get(api_url, json=payload)
            
            if response.status_code == 200:
                    # Parse the response JSON
                    response_json = response.json()

                    # Extract the body from the response
                    images = eval(response_json['body'])

                    # Process the list of image objects
                    if len(images) > 0:
                        for i, obj in enumerate(images):
                            st.write(f"{i+1}. {obj}")
                    else:
                        st.write("No images found.")
            else:
                st.write("Error: Failed to retrieve image.")
            

            if st.button('Delete all images'):
                for image in images:
                    s3.delete_object(Bucket='watermark-project-images-bucket', Key=image)
        
        with watermark:
            st.write("Your watermarks:")
            payload = {
                "username": username,
                "bucket_type": "watermarks"
            }
            response = requests.get(api_url, json=payload)
            if response.status_code == 200:
                    # Parse the response JSON
                    response_json = response.json()

                    # Extract the body from the response
                    watermarks = eval(response_json['body'])
                    
                    # Process the list of image objects
                    if len(watermarks) > 0:
                        for i, obj in enumerate(watermarks):
                            st.write(f"{i+1}. {obj}")
                    else:
                        st.write("No watermarks found.")
            else:
                st.write("Error: Failed to retrieve watermarks.")
            if st.button('Delete all watermarks'):
                for watermark in watermarks:
                    s3.delete_object(Bucket='watermark-project-watermarks-bucket', Key=watermark)


if __name__=='__main__':
    if 'username' not in st.session_state:
        st.session_state['username'] = None
    list_images_page(username=st.session_state['username'])