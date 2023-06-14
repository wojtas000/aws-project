# AWS Project - Watermark App

AWS project for Cloud Computing.

## Project Structure

```
.
├── README.md
│
├── Dockerfile  <- docker image 
│
├── cloudformation-template.yaml <- cloudformation template
│
├── requirements.txt <- python requirements
│
├── cloud_functions <- aws lambda functions
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
│   │   └── ...
│   │
│   └── unit_tests_lambda_functions.py
│
│
├── resources
│   └── ...
│
├── tests   <- unit tests
│   └── test_add_watermark.py
│
└── user_interface <- source code for the streamlit app
    ├── images
    │   └── watermark-logo.png
    │
    ├── main_page.py <- entry script for deploying the app
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