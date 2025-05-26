from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.auth.auth import authenticate_user, create_access_token

class AuthService:
    @staticmethod
    def login(db: Session, email: str, password: str) -> dict:
        if not email.endswith("@l4it.net"):
            raise HTTPException(status_code=400, detail="Email must end with @l4it.net")
        user = authenticate_user(db, email, password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        access_token = create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"} 