from PIL import Image
import io

def add_watermark(main_image, watermark_image, X, Y):

    image_width, image_height = main_image.size
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