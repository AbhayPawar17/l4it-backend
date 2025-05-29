from sqlalchemy.orm import Session
from .models.model import CaseStudy
from .schemas.schema import CaseStudyCreate, CaseStudyUpdate
from typing import List, Optional

def create_case_study(db: Session, case_study: CaseStudyCreate) -> CaseStudy:
    db_case_study = CaseStudy(**case_study.model_dump())
    db.add(db_case_study)
    db.commit()
    db.refresh(db_case_study)
    return db_case_study

def get_case_study(db: Session, case_study_id: int) -> Optional[CaseStudy]:
    return db.query(CaseStudy).filter(CaseStudy.id == case_study_id).first()

def get_case_studies(db: Session, skip: int = 0, limit: int = 10) -> List[CaseStudy]:
    return db.query(CaseStudy).offset(skip).limit(limit).all()

def update_case_study(db: Session, case_study_id: int, case_study: CaseStudyUpdate) -> Optional[CaseStudy]:
    db_case_study = db.query(CaseStudy).filter(CaseStudy.id == case_study_id).first()
    if not db_case_study:
        return None
    for key, value in case_study.model_dump(exclude_unset=True).items():
        setattr(db_case_study, key, value)
    db.commit()
    db.refresh(db_case_study)
    return db_case_study

def delete_case_study(db: Session, case_study_id: int) -> bool:
    db_case_study = db.query(CaseStudy).filter(CaseStudy.id == case_study_id).first()
    if not db_case_study:
        return False
    db.delete(db_case_study)
    db.commit()
    return True