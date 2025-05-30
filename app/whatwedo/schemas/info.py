from pydantic import BaseModel, ConfigDict
from typing import Optional

class InfoBase(BaseModel):
    name: str  # Added name field
    image: Optional[str] = None
    content: str

class InfoCreate(InfoBase):
    user_id: int

class InfoUpdate(InfoBase):
    user_id: int

class InfoOut(InfoBase):
    id: int
    user_id: int
    
    model_config = ConfigDict(from_attributes=True)