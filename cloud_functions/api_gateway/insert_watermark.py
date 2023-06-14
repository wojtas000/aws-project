import json
import base64
from PIL import Image
import io


def lambda_handler(event, context):
    
    """
    This function is called when the user wants to add a watermark to an image.
    It returns a JSON string containing the base64-encoded result image.
    The event contains:
        - main_image: base64-encoded image to which the watermark will be added
        - watermark_image: base64-encoded watermark image
        - X: horizontal position of the watermark (0-10)
        - Y: vertical position of the watermark (0-10)
    """
    
    def add_watermark(main_image, watermark_image, X, Y):

        """
        This function adds a watermark to an image.
        It returns the result image.
        """

        image_width, image_height = main_image.size
        watermark_width, watermark_height = watermark_image.size
    
        # Resize the watermark image to fit within the main image
        if watermark_width > image_width or watermark_height > image_height:
            watermark_image.thumbnail((image_width, image_height), Image.ANTIALIAS)
    
        # Create a new transparent image of the same size as the main image
        transparent_image = Image.new('RGBA', (image_width, image_height), (0, 0, 0, 0))
    
        # Calculate the position to place the watermark
        pos_x = int((image_width - watermark_image.size[0]) * X / 10)
        pos_y = int((image_height - watermark_image.size[1]) * (10 - Y) / 10)
    
        # Composite the watermark image onto the transparent image
        transparent_image.paste(watermark_image, (pos_x, pos_y))
    
        # Blend the transparent image with the main image using alpha_composite
        result_image = Image.alpha_composite(main_image.convert('RGBA'), transparent_image)
    
        return result_image

    try:
        # Retrieve the input parameters from the event
        main_image_base64 = event['main_image']
        watermark_image_base64 = event['watermark_image']
        main_image_bytes = base64.b64decode(main_image_base64)
        watermark_image_bytes = base64.b64decode(watermark_image_base64)
        X = event['X']
        Y = event['Y']

        # Load the main and watermark images from bytes
        main_image = Image.open(io.BytesIO(main_image_bytes))
        watermark_image = Image.open(io.BytesIO(watermark_image_bytes))

        # Call the add_watermark function
        result_image = add_watermark(main_image, watermark_image, X, Y)

        # Save the result image to bytes
        output_buffer = io.BytesIO()
        result_image.save(output_buffer, format='PNG')
        result_image_bytes = output_buffer.getvalue()

        result_image_base64 = base64.b64encode(result_image_bytes).decode('utf-8')

        # Return the result image base64-encoded
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'result_image': result_image_base64})
        }
    
    except Exception as e:
        print('Error adding watermark:', e)
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': 'Failed to add watermark'})
        }
