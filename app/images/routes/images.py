from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.core.database import SessionLocal
from app.images.schemas.images import ImageCreate, ImageUpdate, ImageOut
import os
import shutil
from app.images.crud import create_img,get_img,update_img,delete_img,get_img_by_user
from app.auth.dependencies import get_current_user
from app.auth.models.user import User
from fastapi.responses import JSONResponse
from app.images.model.images import Image
from datetime import datetime


ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
UPLOAD_DIR = "static/uploadedimages"
BASE_URL = "https://l4it.net/api/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ImageOut, status_code=status.HTTP_201_CREATED)
async def create(
   
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
   
    image_path = None
    if image:
        if image.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(status_code=400, detail="Invalid image format. Allowed: jpg, png, gif, webp")
        
        original_name = image.filename
        _, ext = os.path.splitext(original_name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_filename = f"{current_user.id}_{timestamp}{ext}"
        file_location = os.path.join(UPLOAD_DIR, new_filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_path = f"/{file_location.replace(os.sep, '/')}"


    image_data = ImageCreate(
        image=image_path,
        user_id=current_user.id,
        imagename=original_name
    )
    return create_img(db, image_data)
 
@router.get("/", response_model=List[ImageOut])
def read_img(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    img = db.query(Image).offset(skip).limit(limit).all()
    result = []
    for imgs in img:
        user = db.query(User).filter(User.id == imgs.user_id).first()
        author_email = user.email if user else None
        img_dict = imgs.__dict__.copy()
        img_dict["author_email"] = author_email
        if img_dict.get("image"):
            img_dict["image"] = f"{BASE_URL.rstrip('/')}/{img_dict['image'].lstrip('/')}"
        result.append(ImageOut(**img_dict))
    return result



# @router.post("/update/{img_id}", response_model=ImageOut)
# async def update(
#     img_id: int,
#     image: Optional[UploadFile] = File(None),
#     image_path: Optional[str] = Form(None),  # Add this to preserve existing image
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
    
#     img = get_img(db, img_id)
#     if not img:
#         raise HTTPException(status_code=404, detail="Image not found")
#     if img.user_id != current_user.id:
#         raise HTTPException(status_code=403, detail="Not authorized to update access this image.")
    
#     # Handle image logic
#     final_image_path = None
#     if image:
#         # New image uploaded
#         if image.content_type not in ALLOWED_IMAGE_TYPES:
#             raise HTTPException(status_code=400, detail="Invalid image format. Allowed: jpg, png, gif, webp")
#         file_location = os.path.join(UPLOAD_DIR, image.filename)
#         with open(file_location, "wb") as buffer:
#             shutil.copyfileobj(image.file, buffer)
#         final_image_path = f"/{file_location.replace(os.sep, '/')}"
#     elif image_path:
#         # Preserve existing image path sent from frontend
#         final_image_path = image_path
#     else:
#         # Keep the existing image from database
#         final_image_path = img.image

    
#     img_data = ImageUpdate(
       
#         image=final_image_path,  # Use the determined image path
#         user_id=current_user.id,
        
#     )
#     updated = update_img(db, img_id, img_data)
#     return updated


@router.get("/id/{img_id}", response_model=ImageOut)
def read_img_by_id(img_id: int, db: Session = Depends(get_db)):
    img = get_img(db, img_id)
    if not img:
        raise HTTPException(status_code=404, detail="images not found")
    user = db.query(User).filter(User.id == img.user_id).first()
    author_email = user.email if user else None
    img_dict = img.__dict__.copy()
    img_dict["author_email"] = author_email
    if img_dict.get("image"):
        img_dict["image"] = f"{BASE_URL.rstrip('/')}/{img_dict['image'].lstrip('/')}"
        
    
    return ImageOut(**img_dict)


@router.post("/delete/{img_id}", status_code=status.HTTP_200_OK)
def delete(img_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    img = get_img(db, img_id)
    if not img:
        raise HTTPException(status_code=404, detail="Image not found")
    if img.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this Image.")
    success = delete_img(db, img_id)
    return JSONResponse(content={"detail": "Image deleted successfully."}, status_code=200)

@router.get("/user/{user_id}", response_model=List[ImageOut])
def get_img_by_user_route(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view these Images.")
    return get_img_by_user(db, user_id) 