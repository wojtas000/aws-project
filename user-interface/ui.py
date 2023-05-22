import streamlit as st
from PIL import Image
import io

def add_watermark(image_bytes, watermark_bytes, X, Y):
    # Open the main image
    main_image = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    image_width, image_height = main_image.size

    # Open the watermark image
    watermark_image = Image.open(io.BytesIO(watermark_bytes)).convert("RGBA")
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
def main():
    st.title("Watermark App")
    st.write("Choose an option:")

    option = st.radio("Select an option", ("Add Watermark", "Remove Watermark"))

    if option == "Add Watermark":
        # File uploader for the main image
        image_file = st.file_uploader("Upload the main image", type=["png", "jpg", "jpeg"])

        # File uploader for the watermark
        watermark_file = st.file_uploader("Upload the watermark", type=["png"])

        if image_file and watermark_file:
            # Display the uploaded main image
            st.image(image_file, caption="Main Image", use_column_width=True)

            # Display the uploaded watermark image
            st.image(watermark_file, caption="Watermark", use_column_width=True)

            X = st.slider('X', 0, 10, 1)
            Y = st.slider('Y', 0, 10, 1)

            # Button to add watermark
            if st.button("Add Watermark"):
                # Convert file uploader objects to bytes
                image_bytes = image_file.read()
                watermark_bytes = watermark_file.read()

                # Add watermark to the main image
                result_image = add_watermark(image_bytes, watermark_bytes, X, Y)

                # Display the resulting image
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
    main()