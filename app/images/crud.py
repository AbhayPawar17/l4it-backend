from sqlalchemy.orm import Session
from app.images.model.images import Image
from app.images.schemas.images import ImageCreate, ImageUpdate
from typing import List, Optional
import os

def create_img(db: Session, images: ImageCreate) -> Image:
    db_image = Image(**images.dict())
    db.add(db_image)
    db.commit()
    db.refresh(db_image)

    return db_image

def get_img(db: Session, img_id: int) -> Optional[Image]:
    return db.query(Image).filter(Image.id == img_id).first()

# def get_images(db: Session, skip: int = 0, limit: int = 10) -> List[Image]:
#     return db.query(Image).offset(skip).limit(limit).all()

def get_img_by_user(db: Session, user_id: int) -> List[Image]:
    return db.query(Image).filter(Image.user_id == user_id).all()

def update_img(db: Session, img_id: int, image: ImageUpdate) -> Optional[Image]:
    db_img = db.query(Image).filter(Image.id == img_id).first()
    if not db_img:
        return None
    for key, value in image.model_dump(exclude_unset=True).items():
        setattr(db_img, key, value)
    db.commit()
    db.refresh(db_img)
    return db_img

def delete_img(db: Session, img_id: int) -> bool:
    db_img = db.query(Image).filter(Image.id == img_id).first()
    if not db_img:
        return False
    
    if db_img.image:
        file_path = os.path.join(os.getcwd(), db_img.image.lstrip("/"))

        if os.path.exists(file_path):
            os.remove(file_path)

    db.delete(db_img)
    db.commit()
    return True             