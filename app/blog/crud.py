from sqlalchemy.orm import Session
from app.blog.models.blog import Blog
from app.blog.schemas.blog import BlogCreate, BlogUpdate
from typing import List, Optional

def create_blog(db: Session, blog: BlogCreate) -> Blog:
    db_blog = Blog(**blog.model_dump())
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog

def get_blog(db: Session, blog_id: int) -> Optional[Blog]:
    return db.query(Blog).filter(Blog.id == blog_id).first()

def get_blogs(db: Session, skip: int = 0, limit: int = 10) -> List[Blog]:
    return db.query(Blog).offset(skip).limit(limit).all()

def get_blogs_by_user(db: Session, user_id: int) -> List[Blog]:
    return db.query(Blog).filter(Blog.user_id == user_id).all()

def update_blog(db: Session, blog_id: int, blog: BlogUpdate) -> Optional[Blog]:
    db_blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not db_blog:
        return None
    for key, value in blog.model_dump(exclude_unset=True).items():
        setattr(db_blog, key, value)
    db.commit()
    db.refresh(db_blog)
    return db_blog

def delete_blog(db: Session, blog_id: int) -> bool:
    db_blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not db_blog:
        return False
    db.delete(db_blog)
    db.commit()
    return True 