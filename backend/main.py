from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from models.database import get_db
from models.schemas import Documents
from models.model import QueryData
from models.crud import create_document, get_documents
from llama_index.core import GPTVectorStoreIndex, Document
from llama_index.embeddings.openai import OpenAIEmbedding
from services.s3_reader import S3Reader
import fitz
from typing import List
import boto3
import os
from dotenv import load_dotenv

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
aws_region = os.environ.get('AWS_DEFAULT_REGION')
bucket_name = os.environ.get('S3_BUCKET_NAME')

embedding = OpenAIEmbedding(api_key=openai_api_key)

index = None

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

def index_document(filename, text):
    global index
    if index is None:
        doc = Document(text=text, metadata={"filename": filename})          # Create a compatible document format for Indexing
        index = GPTVectorStoreIndex.from_documents([doc], embedding=embedding)      # Use Vector Indexing to index the document
    else:
        s3_reader = S3Reader('your-s3-bucket-name')
        documents = s3_reader.load_data()
        
        # Update the existing index with new documents
        for doc in documents:
            index.insert(doc)
            
    return index

def query_index(query):
    if index is None:
        raise ValueError("Index not initialized. Please upload a document first.")
    query_engine = index.as_query_engine()          # Query the Indexed data
    return query_engine.query(query)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        file_content = await file.read()
        
        upload_to_s3(file)
        
        document = create_document(db, file.filename)

        pdf_document = fitz.open(stream=file_content, filetype="pdf")
        text = "".join([page.get_text() for page in pdf_document])

        doc_id = index_document(file.filename, text)

        return {"filename": file.filename, "document_id": document.id}
    except Exception as e:
        print(f"Detailed error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")


@app.get("/documents", response_model=List[Documents])
def get_all_documents(db: Session = Depends(get_db)):
    return get_documents(db)


@app.post("/query")
async def query_index(request: Request, data: QueryData):
    try:
        response = query_index(data.query)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.1.1.1", port=8001)
