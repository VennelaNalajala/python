import os
import boto3


S3_BUCKET = "gmailstorage"
S3_FOLDER = "gamils"  


s3 = boto3.client("s3")

def upload_attachments(folder="attachments"):
    for filename in os.listdir(folder):
        local_path = os.path.join(folder, filename)
        if os.path.isfile(local_path):
            s3_key = f"{S3_FOLDER}/{filename}"
            try:
                s3.upload_file(local_path, S3_BUCKET, s3_key)
                print(f" Uploaded to S3: s3://{S3_BUCKET}/{s3_key}")
            except Exception as e:
                print(f" Failed to upload {filename}: {e}")

if __name__ == "__main__":
    upload_attachments()