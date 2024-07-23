from pydantic import BaseModel
from datetime import datetime

class DocumentResponse(BaseModel):         # API response model
    id: int
    filename: str
    upload_date: datetime

    class Config:
        orm_mode = True

class QueryData(BaseModel):                # User query model
    query: str