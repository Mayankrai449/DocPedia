import boto3
import os
from dotenv import load_dotenv
load_dotenv()

aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
aws_region = os.environ.get('AWS_DEFAULT_REGION')
bucket_name = os.environ.get('S3_BUCKET_NAME')

def get_s3_client():
    return boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )

def upload_to_s3(file):
    s3 = get_s3_client()
    s3.upload_fileobj(file.file, bucket_name, file.filename)        # Upload file to S3 bucket
    print(f"File '{file.filename}' uploaded to S3 bucket '{bucket_name}'")