from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import SessionLocal
from app.auth.dependencies import get_current_user
from app.auth.models.user import User
from ..models.info import Info
from ..schemas.info import InfoCreate, InfoUpdate, InfoOut
from ..crud.info import (
    create_info,
    get_info,
    get_infos,
    update_info,
    delete_info,
    get_infos_by_user,
)
import os
import shutil

router = APIRouter()
BASE_URL = "https://l4it.net/api/"
UPLOAD_DIR = "static/uploads"
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=InfoOut, status_code=status.HTTP_201_CREATED)
async def create(
    name: str = Form(...),  # Added name parameter
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

    info_data = InfoCreate(
        name=name,  # Added name field
        content=content,
        image=image_path,
        user_id=current_user.id
    )
    return create_info(db, info_data)

@router.get("/", response_model=List[InfoOut])
def read_infos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    infos = get_infos(db, skip, limit)
    result = []
    for info in infos:
        user = db.query(User).filter(User.id == info.user_id).first()
        author_email = user.email if user else None
        info_dict = info.__dict__.copy()
        info_dict["author_email"] = author_email

        if info_dict.get("image"):
            info_dict["image"] = f"{BASE_URL}{info_dict['image']}"
        
        result.append(InfoOut(**info_dict))
    return result

@router.get("/{info_id}", response_model=InfoOut)
def read_info(info_id: int, db: Session = Depends(get_db)):
    info = get_info(db, info_id)
    if not info:
        raise HTTPException(status_code=404, detail="Info not found")
    
    user = db.query(User).filter(User.id == info.user_id).first()
    author_email = user.email if user else None
    info_dict = info.__dict__.copy()
    info_dict["author_email"] = author_email

    # Format image URL
    if info_dict.get("image"):
        info_dict["image"] = f"{BASE_URL}{info_dict['image']}"
    
    return InfoOut(**info_dict)

@router.patch("/{info_id}", response_model=InfoOut)
async def update(
    info_id: int,
    name: str = Form(...),  # Added name parameter
    content: str = Form(...),
    image: Optional[UploadFile] = File(None),
    image_path: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    info = get_info(db, info_id)
    if not info:
        raise HTTPException(status_code=404, detail="Info not found")
    if info.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized.")

    final_image_path = info.image
    if image:
        if image.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(status_code=400, detail="Invalid image format.")
        file_location = os.path.join(UPLOAD_DIR, image.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        final_image_path = f"/{file_location.replace(os.sep, '/')}"
    elif image_path:
        final_image_path = image_path

    updated_data = InfoUpdate(
        name=name,  # Added name field
        content=content,
        image=final_image_path,
        user_id=current_user.id
    )
    return update_info(db, info_id, updated_data)

@router.delete("/{info_id}", status_code=status.HTTP_200_OK)
def delete(info_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    info = get_info(db, info_id)
    if not info:
        raise HTTPException(status_code=404, detail="Info not found")
    if info.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized.")
    delete_info(db, info_id)
    return {"detail": "Info deleted successfully"}

@router.get("/user/{user_id}", response_model=List[InfoOut])
def get_infos_by_user_route(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized.")
    return get_infos_by_user(db, user_id)