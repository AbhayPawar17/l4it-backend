from sqlalchemy.orm import Session
from .models import models
from .schemas import schema

def create_contact_submission(db: Session, submission: schema.ContactSubmissionCreate):
    db_submission = models.ContactSubmission(**submission.model_dump())
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission

def get_contact_submissions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ContactSubmission).offset(skip).limit(limit).all()