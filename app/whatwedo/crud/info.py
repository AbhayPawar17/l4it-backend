from sqlalchemy.orm import Session
from ..models.info import Info
from ..schemas.info import InfoCreate, InfoUpdate
from typing import List, Optional

def create_info(db: Session, info: InfoCreate) -> Info:
    db_info = Info(**info.model_dump())
    db.add(db_info)
    db.commit()
    db.refresh(db_info)
    return db_info

def get_info(db: Session, info_id: int) -> Optional[Info]:
    return db.query(Info).filter(Info.id == info_id).first()

def get_infos(db: Session, skip: int = 0, limit: int = 10) -> List[Info]:
    return db.query(Info).offset(skip).limit(limit).all()

def get_infos_by_user(db: Session, user_id: int) -> List[Info]:
    return db.query(Info).filter(Info.user_id == user_id).all()

def update_info(db: Session, info_id: int, info: InfoUpdate) -> Optional[Info]:
    db_info = db.query(Info).filter(Info.id == info_id).first()
    if not db_info:
        return None
    for key, value in info.model_dump(exclude_unset=True).items():
        setattr(db_info, key, value)
    db.commit()
    db.refresh(db_info)
    return db_info

def delete_info(db: Session, info_id: int) -> bool:
    db_info = db.query(Info).filter(Info.id == info_id).first()
    if not db_info:
        return False
    db.delete(db_info)
    db.commit()
    return True