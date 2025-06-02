from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.core.base import Base

class CaseStudy(Base):
    __tablename__ = "case_studies"
    id = Column(Integer, primary_key=True, index=True)
    image = Column(String(255), nullable=True)
    heading = Column(String(255), nullable=False)
    short_description = Column(String(512), nullable=False)
    content = Column(Text, nullable=False)
    meta_title = Column(String(255), nullable=True)
    meta_description = Column(String(512), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
