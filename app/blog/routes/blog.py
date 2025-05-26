from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.core.database import SessionLocal
from app.blog.schemas.blog import BlogCreate, BlogUpdate, BlogOut
from app.blog.crud import create_blog, get_blog, get_blogs, update_blog, delete_blog, get_blogs_by_user
import os
import shutil
from app.auth.dependencies import get_current_user
from app.auth.models.user import User
from fastapi.responses import JSONResponse
from app.blog.models.blog import Blog

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

@router.post("/", response_model=BlogOut, status_code=status.HTTP_201_CREATED)
async def create(
    heading: str = Form(...),
    short_description: str = Form(...),
    content: str = Form(...),
    meta_title: Optional[str] = Form(None),
    meta_description: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    image_path = None
    if image:
        if image.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(status_code=400, detail="Invalid image format. Allowed: jpg, png, gif, webp")
        file_location = os.path.join(UPLOAD_DIR, image.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_path = f"/{file_location.replace(os.sep, '/')}"
    blog_data = BlogCreate(
        heading=heading,
        short_description=short_description,
        content=content,
        meta_title=meta_title,
        meta_description=meta_description,
        image=image_path,
        user_id=current_user.id
    )
    return create_blog(db, blog_data)

@router.get("/", response_model=List[BlogOut])
def read_blogs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    blogs = db.query(Blog).offset(skip).limit(limit).all()
    result = []
    for blog in blogs:
        user = db.query(User).filter(User.id == blog.user_id).first()
        author_email = user.email if user else None
        blog_dict = blog.__dict__.copy()
        blog_dict["author_email"] = author_email
        result.append(BlogOut(**blog_dict))
    return result

@router.get("/{blog_id}", response_model=BlogOut)
def read_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = get_blog(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    user = db.query(User).filter(User.id == blog.user_id).first()
    author_email = user.email if user else None
    blog_dict = blog.__dict__.copy()
    blog_dict["author_email"] = author_email
    return BlogOut(**blog_dict)

@router.patch("/{blog_id}", response_model=BlogOut)
async def update(
    blog_id: int,
    heading: str = Form(...),
    short_description: str = Form(...),
    content: str = Form(...),
    meta_title: Optional[str] = Form(None),
    meta_description: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    image_path: Optional[str] = Form(None),  # Add this to preserve existing image
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    blog = get_blog(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    if blog.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this blog.")
    
    # Handle image logic
    final_image_path = None
    if image:
        # New image uploaded
        if image.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(status_code=400, detail="Invalid image format. Allowed: jpg, png, gif, webp")
        file_location = os.path.join(UPLOAD_DIR, image.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        final_image_path = f"/{file_location.replace(os.sep, '/')}"
    elif image_path:
        # Preserve existing image path sent from frontend
        final_image_path = image_path
    else:
        # Keep the existing image from database
        final_image_path = blog.image
    
    blog_data = BlogUpdate(
        heading=heading,
        short_description=short_description,
        content=content,
        meta_title=meta_title,
        meta_description=meta_description,
        image=final_image_path,  # Use the determined image path
        user_id=current_user.id
    )
    updated = update_blog(db, blog_id, blog_data)
    return updated

@router.delete("/{blog_id}", status_code=status.HTTP_200_OK)
def delete(blog_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    blog = get_blog(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    if blog.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this blog.")
    success = delete_blog(db, blog_id)
    return JSONResponse(content={"detail": "Blog deleted successfully."}, status_code=200)

@router.get("/user/{user_id}", response_model=List[BlogOut])
def get_blogs_by_user_route(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view these blogs.")
    return get_blogs_by_user(db, user_id) 