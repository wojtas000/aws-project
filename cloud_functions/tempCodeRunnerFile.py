    # def test_list_objects_lambda(self):
    #     event = {
    #         'username': self.username,
    #         'bucket_type': 'images'
    #     }
    #     response = list_objects_lambda(event, None)
    #     self.assertEqual(response['statusCode'], 200)
    #     self.assertEqual(response['body'], '["test_account/test_image.png"]')