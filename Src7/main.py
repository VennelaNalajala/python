import boto3
from io import BytesIO
import fitz
from transform import transform
from archieve import move
s3=boto3.client('s3')
bucket_name='vennelaresume'
path='resumes/'
files=s3.list_objects_v2(Bucket=bucket_name,Prefix=path)
pdf_list=[file['Key'] for file in files.get('Contents',[]) if file['Key'].endswith('.pdf')]
for key in pdf_list:
    stream=BytesIO()
    s3.download_fileobj(bucket_name,key,stream)
    stream.seek(0)
    doc=fitz.open(stream=stream,filetype="pdf")
    text=''
    for page in doc:
        text+=page.get_text("text")
        
    transform(text)
    move(bucket_name,key)
    



