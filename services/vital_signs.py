from sqlalchemy.orm import Session
from models.base import VitalSigns
from schemas.vital_signs import VitalSignsCreate, VitalSignsResponse, VitalSignsUpdate
from typing import List
from fastapi import status


def read_vital_signs(db: Session):
    vitals: List[VitalSigns] = db.query(VitalSigns).all()
    if vitals is None:
        return None, status.HTTP_404_NOT_FOUND
    if len(vitals) == 0:
        return [], status.HTTP_204_NO_CONTENT
    return [VitalSignsResponse(**vs.__dict__) for vs in vitals], status.HTTP_200_OK


def create_vital_sign(db: Session, patient_id:int, vital_sign: VitalSignsCreate):
    db_vital_sign: VitalSigns = VitalSigns(**vital_sign.model_dump(), patient_id=patient_id)
    db.add(db_vital_sign)
    db.commit()
    db.refresh(db_vital_sign)
    return VitalSignsResponse(**db_vital_sign.__dict__), status.HTTP_201_CREATED


def read_vital_sign(db: Session, vital_sign_id: int):
    if not_exists_vs_id(db, vital_sign_id):
        return None, status.HTTP_404_NOT_FOUND
    vs: VitalSigns = db.query(VitalSigns).filter(
        VitalSigns.id == vital_sign_id
    ).first()
    return VitalSignsResponse(**vs.__dict__), status.HTTP_200_OK


def replace_vital_signs(db: Session, patient_id: int, new_vs: VitalSignsUpdate):
    if not_exists_patient_id(db, patient_id):
        return None, status.HTTP_404_NOT_FOUND
    db_vs = db.query(VitalSigns).filter(
        VitalSigns.patient_id == patient_id
    ).first()

    db_vs.O2_saturation = new_vs.O2_saturation
    db_vs.blood_pressure = new_vs.blood_pressure
    db_vs.hearth_rate = new_vs.hearth_rate
    db_vs.created_at = new_vs.created_at
    db.commit()
    return VitalSignsResponse(**db_vs.__dict__), status.HTTP_200_OK


def remove_vital_sign(db: Session, vital_sign_id: int):
    if not_exists_vs_id(db, vital_sign_id):
        return None, status.HTTP_404_NOT_FOUND
    db.query(VitalSigns).filter(
        VitalSigns.id == vital_sign_id
    ).delete()
    db.commit()
    return None, status.HTTP_200_OK


def get_vital_signs_by_patient_id(db: Session, patient_id: int):
    return db.query(VitalSigns).filter(VitalSigns.patient_id == patient_id).all()


def not_exists_vs_id(db: Session, vital_sign_id: int):
    return db.query(VitalSigns).filter(VitalSigns.id == vital_sign_id).first() is None


def not_exists_patient_id(db: Session, patient_id: int):
    return db.query(VitalSigns).filter(VitalSigns.patient_id == patient_id).first() is None
