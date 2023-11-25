from sqlalchemy import or_, select
from sqlalchemy.orm import Session
from models.base import Appointment, Doctor, DoctorPatients, Patient
from schemas.appointment import AppointmentSchema
from typing import List

def post_appointment(db: Session, appointment: AppointmentSchema) -> Appointment:
    db_appointment = Appointment(**appointment.model_dump())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def get_appointments(db: Session) -> List[Appointment]:
    return db.query(Appointment).all()

'''necesito un metodo que con el doctor_patient_id me devuelva todas las citas de ese doctor o paciente
tengo una tabla que se llama doctor_patient que tiene un id y un doctor_id y un patient_id y ese
'''
def get_appointments_by_user_id(db: Session, user_id: int):
    stmt = (select(Appointment)
            .join(DoctorPatients)
            .join(Doctor, DoctorPatients.c.doctor_id == Doctor.id)
            .join(Patient, DoctorPatients.c.patient_id == Patient.id)
            .where(or_(Doctor.user_id == user_id, Patient.user_id == user_id)))
    appointments = db.execute(stmt).scalars().all()
    return appointments