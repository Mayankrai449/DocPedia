from fastapi import FastAPI, File, Form, UploadFile, HTTPException, Request, Depends, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from llama_index_client import OpenAiEmbedding
from sqlalchemy.orm import Session
from models.database import get_db
from models.schemas import Document
from models.model import QueryData
from models.crud import create_document, get_documents
from llama_index.core import GPTVectorStoreIndex, SimpleDirectoryReader
from typing import List, Annotated
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
    file_location = f"./data/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_data = await file.read()
        file_object.write(file_data)

    # Save document metadata to the database
    document = create_document(db, file.filename)

    # Create a new index with all documents in the data directory
    global index

    documents = SimpleDirectoryReader('./data').load_data()

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
