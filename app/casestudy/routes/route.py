from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import SessionLocal
from ..schemas.schema import CaseStudyCreate, CaseStudyUpdate, CaseStudyOut
from ..logic import (
    create_case_study, 
    get_case_study, 
    get_case_studies, 
    update_case_study, 
    delete_case_study
)
import os
import shutil

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=CaseStudyOut, status_code=status.HTTP_201_CREATED)
async def create(
    heading: str = Form(...),
    short_description: str = Form(...),
    content: str = Form(...),
    meta_title: Optional[str] = Form(None),
    meta_description: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    image_path = None
    if image:
        if image.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(status_code=400, detail="Invalid image format. Allowed: jpg, png, gif, webp")
        file_location = os.path.join(UPLOAD_DIR, image.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_path = f"/{file_location.replace(os.sep, '/')}"
    case_study_data = CaseStudyCreate(
        heading=heading,
        short_description=short_description,
        content=content,
        meta_title=meta_title,
        meta_description=meta_description,
        image=image_path
    )
    return create_case_study(db, case_study_data)

@router.get("/", response_model=List[CaseStudyOut])
def read_case_studies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_case_studies(db, skip=skip, limit=limit)

@router.get("/{case_study_id}", response_model=CaseStudyOut)
def read_case_study(case_study_id: int, db: Session = Depends(get_db)):
    case_study = get_case_study(db, case_study_id)
    if not case_study:
        raise HTTPException(status_code=404, detail="Case study not found")
    return case_study

@router.patch("/{case_study_id}", response_model=CaseStudyOut)
async def update(
    case_study_id: int,
    heading: str = Form(...),
    short_description: str = Form(...),
    content: str = Form(...),
    meta_title: Optional[str] = Form(None),
    meta_description: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    image_path: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    case_study = get_case_study(db, case_study_id)
    if not case_study:
        raise HTTPException(status_code=404, detail="Case study not found")
    
    final_image_path = None
    if image:
        if image.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(status_code=400, detail="Invalid image format. Allowed: jpg, png, gif, webp")
        file_location = os.path.join(UPLOAD_DIR, image.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        final_image_path = f"/{file_location.replace(os.sep, '/')}"
    elif image_path:
        final_image_path = image_path
    else:
        final_image_path = case_study.image
    
    case_study_data = CaseStudyUpdate(
        heading=heading,
        short_description=short_description,
        content=content,
        meta_title=meta_title,
        meta_description=meta_description,
        image=final_image_path
    )
    updated = update_case_study(db, case_study_id, case_study_data)
    return updated

@router.delete("/{case_study_id}", status_code=status.HTTP_200_OK)
def delete(case_study_id: int, db: Session = Depends(get_db)):
    success = delete_case_study(db, case_study_id)
    if not success:
        raise HTTPException(status_code=404, detail="Case study not found")
    return {"detail": "Case study deleted successfully."}