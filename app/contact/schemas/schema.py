from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class ContactSubmissionCreate(BaseModel):
    company_name: Optional[str] = None
    num_employees: Optional[str] = None
    first_name: str
    last_name: str
    business_email: EmailStr
    phone_number: Optional[str] = None
    referral_source: Optional[str] = None
    message: str
    services_needed: str
    how_did_u_hear_us:Optional[str] = None

class ContactSubmissionOut(ContactSubmissionCreate):
    id: int
    submission_date: datetime

    class Config:
        from_attributes = True