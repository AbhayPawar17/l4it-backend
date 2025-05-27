from pydantic import BaseModel, ConfigDict
from typing import Optional

class MSPServiceBase(BaseModel):
    image: Optional[str] = None
    content: str

class MSPServiceCreate(MSPServiceBase):
    user_id: int

class MSPServiceUpdate(MSPServiceBase):
    user_id: int

class MSPServiceOut(MSPServiceBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
