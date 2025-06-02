from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from app.core.base import Base

class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    image = Column(String(255), nullable=True)
    heading = Column(String(255), nullable=False)
    short_description = Column(String(512), nullable=False)
    content = Column(Text, nullable=False)
    meta_title = Column(String(255), nullable=True)
    meta_description = Column(String(512), nullable=True)
    type = Column(String, nullable=False) 
    slug = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
