from pydantic import BaseModel
from datetime import datetime

class Documents(BaseModel):
    id: int
    filename: str
    upload_date: datetime

    class Config:
        orm_mode = True