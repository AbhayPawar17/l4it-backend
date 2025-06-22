from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional

class BlogBase(BaseModel):
    image: Optional[str] = None
    heading: str
    type: Optional[str] = None
    slug: Optional[str] = None
    short_description: str
    content: str
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    blog_data_raw : Optional[str] = None

class BlogCreate(BlogBase):
    user_id: int

class BlogUpdate(BlogBase):
    user_id: int 

class BlogOut(BlogBase):
    id: int
    user_id: int
    author_email: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
