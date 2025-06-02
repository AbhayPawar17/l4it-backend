from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional

class InfoBase(BaseModel):
    name: str  
    image: Optional[str] = None
    content: str

class InfoCreate(InfoBase):
    user_id: int

class InfoUpdate(InfoBase):
    user_id: int

class InfoOut(InfoBase):
    id: int
    user_id: int
    author_email: Optional[str] = None  
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)