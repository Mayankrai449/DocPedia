from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .database import Base, engine  # Import engine from database
from pydantic import BaseModel

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    upload_date = Column(DateTime, server_default=func.now())

# Create tables
Base.metadata.create_all(bind=engine)

class QueryData(BaseModel):
    query: str