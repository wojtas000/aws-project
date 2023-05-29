import streamlit as st
from PIL import Image
import io
import boto3


# Tworzenie klienta S3
s3 = boto3.client('s3')


def remove_watermark(image_bytes):
    # Load the image
    image = Image.open(io.BytesIO(image_bytes)).convert("RGBA")

    # TODO: Implement watermark removal logic here
    # Replace the code below with your watermark removal algorithm

    # Simply return the original image for now
    return image



def remove_watermark_page(username):
    if st.session_state['username'] is None:
        st.write('You have to sign in first!')
        st.stop()
    else:
        username = st.session_state['username']
        st.title("Remove Watermark")

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
    remove_watermark_page(username=st.session_state['username'])