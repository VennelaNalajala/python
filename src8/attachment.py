import boto3
import uuid
import os

def upload_to_s3(file_path, bucket_name):
    s3 = boto3.client('s3')
    key = f"{uuid.uuid4()}_{os.path.basename(file_path)}"
    s3.upload_file(file_path, bucket_name, key)
    return f"https://{bucket_name}.s3.amazonaws.com/{key}"
