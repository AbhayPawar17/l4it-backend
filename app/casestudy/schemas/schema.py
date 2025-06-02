from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class CaseStudyBase(BaseModel):
    image: Optional[str] = None
    heading: str
    short_description: str
    content: str
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None

class CaseStudyCreate(CaseStudyBase):
    pass

class CaseStudyUpdate(CaseStudyBase):
    pass

class CaseStudyOut(CaseStudyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)