from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional

class ImageBase(BaseModel):
    image: Optional[str] = None
    
class ImageCreate(ImageBase):
    user_id: int

class ImageUpdate(ImageBase):
    user_id: int 

class ImageOut(ImageBase):
    id: int
    user_id: int
    author_email: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
