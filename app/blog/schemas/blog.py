from pydantic import BaseModel, ConfigDict
from typing import Optional

class BlogBase(BaseModel):
    image: Optional[str] = None
    heading: str
    short_description: str
    content: str
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None

class BlogCreate(BlogBase):
    user_id: int

class BlogUpdate(BlogBase):
    user_id: int

class BlogOut(BlogBase):
    id: int
    user_id: int
    author_email: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
