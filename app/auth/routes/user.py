from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.auth.models.user import User
from app.auth.schemas.user import UserCreate, UserLogin, UserOut
from app.auth.auth import get_password_hash
from typing import Generator
from app.auth.auth_service import AuthService

router = APIRouter()

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if not user.email.endswith("@l4it.net"):
        raise HTTPException(status_code=400, detail="Email must end with @l4it.net")
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    return AuthService.login(db, user.email, user.password) 