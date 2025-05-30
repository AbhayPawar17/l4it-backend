from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.core.base import Base

class MSPService(Base):
    __tablename__ = "msp_services"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)  
    image = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)