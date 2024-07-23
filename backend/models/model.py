from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .database import Base, engine
from pydantic import BaseModel

class Documents(Base):      # DB Doc model
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    upload_date = Column(DateTime, server_default=func.now())

Base.metadata.create_all(bind=engine)