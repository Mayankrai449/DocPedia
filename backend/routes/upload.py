from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from models.database import get_db
from models.crud import create_document
from services.s3_upload import upload_to_s3
from services.query_indexing import index_document
import fitz

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        file_content = await file.read()
        
        if not upload_to_s3(file_content, file.filename):                               # Upload the file to S3
            raise HTTPException(status_code=500, detail="Failed to upload file to S3")
        
        document = create_document(db, file.filename)

        pdf_document = fitz.open(stream=file_content, filetype="pdf")
        text = "".join([page.get_text() for page in pdf_document])              # Extract text from PDF for intial indexing

        doc_id = index_document(file.filename, text)
        if doc_id is None:
            raise HTTPException(status_code=500, detail="Failed to index document")
        return {"filename": file.filename, "document_id": document.id}
    except Exception as e:
        print(f"Detailed error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")