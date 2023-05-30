import json
import base64
from PIL import Image
import io
# from add_watermark import add_watermark

def lambda_handler(event, context):
    
    def add_watermark(main_image, watermark_image, X, Y):
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

    
    # Retrieve the input parameters from the event
    main_image_base64 = event['main_image']
    watermark_image_base64 = event['watermark_image']
    main_image_bytes = base64.b64decode(main_image_base64)
    watermark_image_bytes = base64.b64decode(watermark_image_base64)
    X = event['X']
    Y = event['Y']

    # Load the main image from bytes
    main_image = Image.open(io.BytesIO(main_image_bytes))

    # Load the watermark image from bytes
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
