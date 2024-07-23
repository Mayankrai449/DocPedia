import io
import PyPDF2
from llama_index.core import Document
from llama_index.core.readers.base import BaseReader
from services.s3_upload import bucket_name, get_s3_client
import botocore

class S3Reader(BaseReader):
    def __init__(self):
        self.bucket_name = bucket_name
        self.s3 = get_s3_client()

    def load_data(self):
        """Load data from S3 bucket"""
        documents = []
        try:
            response = self.s3.list_objects_v2(Bucket=self.bucket_name)

            for obj in response.get('Contents', []):
                file_key = obj['Key']
                try:

                    get_response = self.s3.get_object(Bucket=self.bucket_name, Key=file_key)    # Get the file from S3
                    file_content = get_response['Body'].read()
                    
                    if file_key.lower().endswith('.pdf'):
                        text = self.process_pdf(file_content)   # Process the PDF file
                    else:
                        text = file_content.decode('utf-8')
                        
                    if not text.strip():                                    # Check if text is empty
                        print(f"Warning: File {file_key} contains no text")
                        continue

                    documents.append(Document(text=text, metadata={"filename": file_key}))
                    
                except botocore.exceptions.ClientError as e:                                    # Handle S3 ClientError
                    print(f"S3 ClientError for file {file_key}: {e.response['Error']}")
                except Exception as file_error:
                    print(f"Error processing file {file_key}: {str(file_error)}")

            return documents
        except Exception as e:
            print(f"Error loading data from S3: {str(e)}")
            return []

    def process_pdf(self, content):
        """Extract text from PDF file"""
        try:
            pdf_file = io.BytesIO(content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            if len(pdf_reader.pages) == 0:      # Check for no pages
                print("PDF has no pages")
                return ""

            text = ""
            for i, page in enumerate(pdf_reader.pages):         # Extracting text from each page
                try:
                    page_text = page.extract_text()     
                    if page_text:
                        text += page_text
                    else:
                        print(f"Page {i} is empty or could not be read")
                except Exception as page_error:
                    print(f"Error extracting text from page {i}: {str(page_error)}")

            if not text:
                print("No text could be extracted from the PDF")
            
            return text
        except Exception as pdf_error:
            print(f"Error processing PDF: {str(pdf_error)}")
            return ""