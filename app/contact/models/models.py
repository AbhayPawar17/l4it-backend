from app.core.database import Base
from sqlalchemy import Column, String, Integer, DateTime, Text
from datetime import datetime

class ContactSubmission(Base):
    __tablename__ = "contact_submissions"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(100), nullable=True)
    num_employees = Column(String(50), nullable=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    business_email = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=True)
    referral_source = Column(String(100), nullable=True)
    message = Column(Text, nullable=False)
    services_needed = Column(String(200), nullable=False)
    submission_date = Column(DateTime, default=datetime.utcnow)