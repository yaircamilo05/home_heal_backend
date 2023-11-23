from schemas.doctor import Doctor as DoctorSchema
from models.base import Doctor

def create_doctor(doctor: DoctorSchema, db):
    print('llegue a crear doctor')
    
    doctor_db = Doctor(**doctor.model_dump())
    
    db.add(doctor_db)
    db.commit()
    db.refresh(doctor_db)
    return doctor_db


def get_doctor_by_user_id(user_id: int, db):
    doctor = db.query(Doctor).filter(Doctor.user_id == user_id).first()
    return doctor


def put_doctor(id: int, doctor: DoctorSchema, db):
    print('llegue a editar doctor')
    db_doctor: Doctor = db.query(Doctor).filter(Doctor.id == id).first()
    if db_doctor is None:
        return None
    
    for attr, value in doctor.model_dump().items():
        setattr(db_doctor, attr, value)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor