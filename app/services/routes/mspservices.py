from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import SessionLocal
from app.auth.dependencies import get_current_user
from app.auth.models.user import User
from ..models.mspservices import MSPService
from ..schemas.mspservices import MSPServiceCreate, MSPServiceUpdate, MSPServiceOut
from ..mspcrud import (
    create_service,
    get_service,
    get_services,
    update_service,
    delete_service,
    get_services_by_user,
)
import os
import shutil

router = APIRouter()
UPLOAD_DIR = "static/uploads"
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=MSPServiceOut, status_code=status.HTTP_201_CREATED)
async def create(
    content: str = Form(...),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    image_path = None
    if image:
        if image.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(status_code=400, detail="Invalid image format.")
        file_location = os.path.join(UPLOAD_DIR, image.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_path = f"/{file_location.replace(os.sep, '/')}"

    service_data = MSPServiceCreate(
        content=content,
        image=image_path,
        user_id=current_user.id
    )
    return create_service(db, service_data)

@router.get("/", response_model=List[MSPServiceOut])
def read_services(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_services(db, skip, limit)

@router.get("/{service_id}", response_model=MSPServiceOut)
def read_service(service_id: int, db: Session = Depends(get_db)):
    service = get_service(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

@router.patch("/{service_id}", response_model=MSPServiceOut)
async def update(
    service_id: int,
    content: str = Form(...),
    image: Optional[UploadFile] = File(None),
    image_path: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = get_service(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    if service.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized.")

    final_image_path = service.image
    if image:
        if image.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(status_code=400, detail="Invalid image format.")
        file_location = os.path.join(UPLOAD_DIR, image.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        final_image_path = f"/{file_location.replace(os.sep, '/')}"

    elif image_path:
        final_image_path = image_path

    updated_data = MSPServiceUpdate(
        content=content,
        image=final_image_path,
        user_id=current_user.id
    )
    return update_service(db, service_id, updated_data)

@router.delete("/{service_id}", status_code=status.HTTP_200_OK)
def delete(service_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = get_service(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    if service.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized.")
    delete_service(db, service_id)
    return {"detail": "Service deleted successfully"}

@router.get("/user/{user_id}", response_model=List[MSPServiceOut])
def get_services_by_user_route(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized.")
    return get_services_by_user(db, user_id)
