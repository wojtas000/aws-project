import PIL
from PIL import Image, ImageEnhance

# load file "1.jpeg"
img1 = PIL.Image.open("1.jpeg")
# load 2.jpeg
img2 = PIL.Image.open("2.webp")


import requests

url = "https://zylalabs.com/api/333/watermark+and+handwriting+remover+api/268/remover"
data = {
    # Provide any required parameters or data in the request body
    # Example: 'key': 'value'
}

# Specify the path to your image file
image_path = "1.jpeg"

# Read the image file content before closing it
with open(image_path, "rb") as image_file:
    image_content = image_file.read()

# Include the image content in the 'files' parameter as a tuple
files = {"image": ("image.jpg", image_content)}

response = requests.post(url, data=data, files=files)

# Check the response status code
if response.status_code == 200:
    # Request was successful
    print("POST request successful!")
    print("Response:", response.text)
else:
    # Request failed
    print("POST request failed with status code:", response.status_code)
