# AWS Project - Watermark App

AWS project for Cloud Computing.

## Project Structure

```
.
├── Dockerfile
│
├── README.md
│
├── cloudformation-template.yaml
│
├── requirements.txt
│
├── cloud_functions
│   ├── api_gateway
│   │   ├── display_user_history.py
│   │   ├── insert_watermark.py
│   │   ├── list_images.py
│   │   └── upload_image.py
│   │
│   ├── dynamoDB_S3_connectivity
│   │   ├── delete_image_data_and_update_dynamoDB.py
│   │   ├── send_image_data_to_dynamoDB.py
│   │   ├── test_event_delete.json
│   │   └── test_event_send.json
│   │
│   ├── test_images
│   │   ├── image.png
│   │   └── watermark.png
│   │
│   └── unit_tests_lambda_functions.py
│
│
├── resources
│   └── ...
│
├── tests
│   └── test_add_watermark.py
│
└── user_interface
    ├── images
    │   └── watermark-logo.png
    │
    ├── main_page.py
    │
    └── pages
        ├── 1_upload_images.py
        ├── 2_list_images.py
        ├── 3_apply_watermark.py
        ├── 4_remove_watermark.py
        ├── 5_User_history.py
        │
        └── api_and_functions
            ├── add_remove_watermark.py
            ├── api_requests.py
            ├── get_secrets.py
            └── watermark_remover.py
```