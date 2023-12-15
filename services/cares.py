from models.base import Cares, DoctorPatients, Doctor
from schemas.cares import CaresGet, CaresCreate, Care
from schemas.user import User
from sqlalchemy.orm import joinedload
from schemas.doctor import DoctorWithUser


def create_care(care: CaresCreate, db):

    doctor_patient = db.query(DoctorPatients).filter(
        DoctorPatients.c.doctor_id == care.doctor_id,
        DoctorPatients.c.patient_id == care.patient_id
    ).first()

    if doctor_patient is None:
        return None
    care_bd = Cares(description=care.description,
                    doctor_patients_id=doctor_patient.id)
    db.add(care_bd)
    db.commit()
    db.refresh(care_bd)
    return care_bd


def get_cares_by_patient_id(id: int, db):
    cares_bd: Cares = db.query(Cares).options(joinedload(Cares.doctor).joinedload(Doctor.user)).join(
        DoctorPatients, Cares.doctor_patients_id == DoctorPatients.c.id).filter(DoctorPatients.c.patient_id == id).all()
    for cares in cares_bd:
        cares.doctor[0].user.password = None
    return cares_bd


def get_cares_by_doctor_id(id: int, db) -> list[CaresGet]:
    cares_bd = db.query(Cares).join(DoctorPatients, Cares.doctor_patient_id ==
                                    DoctorPatients.doctor_id).filter(DoctorPatients.doctor_id == id).all()
    cares = []
    for care in cares_bd:
        cares.append(CaresGet(**care.dict()))
    return cares


def delete_care(id: int, db) -> bool:
    care = db.query(Cares).filter(Cares.id == id).first()

    if care:
        db.delete(care)
        db.commit()
        return True
    return False
