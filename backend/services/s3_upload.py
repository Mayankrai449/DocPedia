import boto3
import os
from dotenv import load_dotenv
load_dotenv()

aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
aws_region = os.environ.get('AWS_DEFAULT_REGION')
bucket_name = os.environ.get('S3_BUCKET_NAME')

def get_s3_client():
    """Return S3 client"""
    return boto3.client(                          # Create an S3 client
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )

def upload_to_s3(file_content, filename):
    """Upload file to S3 bucket"""
    s3 = get_s3_client()
    try:
        s3.put_object(Body=file_content, Bucket=bucket_name, Key=filename)      # Uploading File Object to S3
        print(f"File '{filename}' uploaded to S3 bucket '{bucket_name}'")
        return True
    except Exception as e:
        print(f"Error uploading file to S3: {str(e)}")
        return False