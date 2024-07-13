from llama_index.core import Document
from llama_index.core.readers.base import BaseReader
import boto3

class S3Reader(BaseReader):
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3 = boto3.client('s3')

    def load_data(self):
        documents = []
        response = self.s3.list_objects_v2(Bucket=self.bucket_name)
        
        for obj in response.get('Contents', []):
            file_key = obj['Key']
            file_content = self.s3.get_object(Bucket=self.bucket_name, Key=file_key)['Body'].read().decode('utf-8')
            documents.append(Document(text=file_content, metadata={"filename": file_key}))
        
        return documents