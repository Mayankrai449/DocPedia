from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.model import QueryData
from models.database import get_db
from models.schemas import Documents
from models.crud import get_documents
from typing import List
from services.query_indexing import query_index

router = APIRouter()

@router.get("/documents", response_model=List[Documents])
def get_all_documents(db: Session = Depends(get_db)):
    '''Show history of Documents used'''
    try:
        documents = get_documents(db)
        if documents is None:
            raise HTTPException(status_code=404, detail="Documents not found")
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving documents")


@router.post("/query")
async def query_data(data: QueryData):
    '''Input user query and return a response'''
    try:
        response = query_index(data.query)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
