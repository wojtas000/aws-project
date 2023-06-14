import unittest
import base64
from api_gateway.upload_image import lambda_handler as upload_image_lambda
from api_gateway.display_user_history import lambda_handler as user_history_lambda
from api_gateway.insert_watermark import lambda_handler as add_watermark_lambda
from api_gateway.list_images import lambda_handler as list_objects_lambda


def read_image_to_base64(image_path):
    """
    Read image from file and convert it to base64
    """
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
        base64_data = base64.b64encode(image_data).decode('utf-8')
        return base64_data


class ColoredTestResult(unittest.TextTestResult):
    """
    Class for colored test results
    """
    def addSuccess(self, test):
        super().addSuccess(test)
        self.stream.writeln("\u2714 " + self.getDescription(test))


class TestLambdaFunctions(unittest.TestCase):
    """
    Class for testing lambda functions
    """

    image = read_image_to_base64('./test_images/image.png')
    watermark = read_image_to_base64('./test_images/watermark.png')
    username = 'test_account'

    def test_upload_image_lambda1(self):
        
        """
        Test api_gateway.upload_image lambda function for uploading image to S3
        """

        event = {
            'body': self.image,
            'name': 'test_image.png',
            'bucket_type': 'images',
            'username': self.username
        }
        response = upload_image_lambda(event, None)
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['body'], '{"message": "Image uploaded successfully"}')

    def test_upload_image_lambda2(self):
        
        """
        Test api_gateway.upload_image lambda function for uploading watermark to S3
        """

        event = {
            'body': self.watermark,
            'name': 'test_watermark.png',
            'bucket_type': 'watermarks',
            'username': self.username
        }
        response = upload_image_lambda(event, None)
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['body'], '{"message": "Image uploaded successfully"}')

    def test_user_history_lambda(self):

        """
        Test api_gateway.display_user_history lambda function for correctness of displaying user history
        """

        event = {
            'user_login': self.username
        }
        response = user_history_lambda(event, None)
        self.assertEqual(response['statusCode'], 200)

    def test_add_watermark_lambda(self):

        """
        Test api_gateway.insert_watermark lambda function for correctness of adding watermark to image
        """

        event = {
            'main_image': self.image,
            'watermark_image': self.watermark,
            'X': 1,
            'Y': 2
        }
        response = add_watermark_lambda(event, None)
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['headers']['Content-Type'], 'application/json')
        self.assertIn('result_image', response['body'])

    def test_list_objects_lambda1(self):

        """
        Test api_gateway.list_images lambda function for correctness of listing images
        """

        event = {
            'username': self.username,
            'bucket_type': 'images'
        }
        response = list_objects_lambda(event, None)
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['body'], '["test_account/test_image.png"]')

    def test_list_objects_lambda2(self):

        """
        Test api_gateway.list_images lambda function for correctness of listing watermarks
        """
        
        event = {
            'username': self.username,
            'bucket_type': 'watermarks'
        }
        response = list_objects_lambda(event, None)
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['body'], '["test_account/test_watermark.png"]')


if __name__ == '__main__':
    unittest.main(testRunner=unittest.TextTestRunner(resultclass=ColoredTestResult))
