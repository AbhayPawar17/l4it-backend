from sqlalchemy.orm import Session
from .models.mspservices import MSPService
from .schemas.mspservices import MSPServiceCreate, MSPServiceUpdate
from typing import List, Optional

def create_service(db: Session, service: MSPServiceCreate) -> MSPService:
    db_service = MSPService(**service.model_dump())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

def get_service(db: Session, service_id: int) -> Optional[MSPService]:
    return db.query(MSPService).filter(MSPService.id == service_id).first()

def get_services(db: Session, skip: int = 0, limit: int = 10) -> List[MSPService]:
    return db.query(MSPService).offset(skip).limit(limit).all()

def get_services_by_user(db: Session, user_id: int) -> List[MSPService]:
    return db.query(MSPService).filter(MSPService.user_id == user_id).all()

def update_service(db: Session, service_id: int, service: MSPServiceUpdate) -> Optional[MSPService]:
    db_service = db.query(MSPService).filter(MSPService.id == service_id).first()
    if not db_service:
        return None
    for key, value in service.model_dump(exclude_unset=True).items():
        setattr(db_service, key, value)
    db.commit()
    db.refresh(db_service)
    return db_service

def delete_service(db: Session, service_id: int) -> bool:
    db_service = db.query(MSPService).filter(MSPService.id == service_id).first()
    if not db_service:
        return False
    db.delete(db_service)
    db.commit()
    return True
