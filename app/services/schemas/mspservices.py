from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class MSPServiceBase(BaseModel):
    name: str  # Added service name field
    image: Optional[str] = None
    content: str

class MSPServiceCreate(MSPServiceBase):
    user_id: int

class MSPServiceUpdate(MSPServiceBase):
    user_id: int

class MSPServiceOut(MSPServiceBase):
    id: int
    user_id: int
    author_email: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)