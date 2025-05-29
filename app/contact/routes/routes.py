from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from ..logic import create_contact_submission, get_contact_submissions
from ..schemas import schema

router = APIRouter()

@router.post("/submit", response_model=schema.ContactSubmissionOut)
async def submit_contact_form(
    submission: schema.ContactSubmissionCreate,
    db: Session = Depends(get_db)
):
    """Submit a new contact form"""
    return create_contact_submission(db, submission)

@router.get("/submissions", response_model=list[schema.ContactSubmissionOut])
async def get_submissions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all contact submissions (for admin purposes)"""
    return get_contact_submissions(db, skip=skip, limit=limit)