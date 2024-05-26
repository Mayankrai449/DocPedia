from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from llama_index_client import OpenAiEmbedding, S3Reader
from sqlalchemy.orm import Session
from models.database import get_db
from models.schemas import Document
from models.model import QueryData
from models.crud import create_document, get_documents
from llama_index.core import GPTVectorStoreIndex
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

index = None

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Upload file to S3 bucket
    s3 = boto3.client('s3')
    bucket_name = 'your-bucket-name'
    object_key = f'uploaded-files/{file.filename}'

    try:
        s3.upload_fileobj(file.file, bucket_name, object_key)
        print(f"File '{file.filename}' uploaded to S3 bucket '{bucket_name}'")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file to S3: {str(e)}")

    # Save document metadata to the database
    document = create_document(db, file.filename)

    # Create a new index with documents from S3 bucket
    global index
    s3_reader = S3Reader(bucket_name, prefix='uploaded-files/')
    documents = s3_reader.load_data()
    embedding = OpenAiEmbedding(api_key=openai_api_key)
    index = GPTVectorStoreIndex.from_documents(documents, embedding=embedding)

    return {"filename": file.filename, "document_id": document.id}

@app.get("/documents", response_model=List[Document])
def get_all_documents(db: Session = Depends(get_db)):
    return get_documents(db)

@app.post("/query")
async def query_index(request: Request, data: QueryData):
    try:
        if index is None:
            raise HTTPException(status_code=500, detail="Index not initialized.")
        
        query_engine = index.as_query_engine()

        response = query_engine.query(data.query)
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8222)
