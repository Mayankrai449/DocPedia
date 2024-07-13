from sqlalchemy.orm import Session
import models.model as models
from datetime import datetime, timezone

def create_document(db: Session, filename: str):
    document = models.Documents(filename=filename, upload_date=datetime.now(timezone.utc))
    db.add(document)
    db.commit()
    db.refresh(document)
    return document

def get_documents(db: Session):
    return db.query(models.Documents).all()