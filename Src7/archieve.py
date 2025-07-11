import boto3
import os
def move(source_bucket,source_key):
    destination_bucket='vennelaresume'
    destination_path='archieve/'
    destination_key=os.path.join(destination_path,os.path.basename(source_key))
    s3=boto3.resource('s3')
    copy_source={
        'Bucket':source_bucket,
        'Key':source_key
    }
    s3.meta.client.copy(copy_source,destination_bucket,destination_key)
    s3.Object(source_bucket, source_key).delete()

    print(f"Object moved from s3://{source_bucket}/{source_key} to s3://{destination_bucket}/{destination_key}")