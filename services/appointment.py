from datetime import datetime
from sqlalchemy import AliasedReturnsRows, or_, select
from sqlalchemy.orm import Session
from models.base import Appointment, Doctor, DoctorPatients, Patient, User
from schemas.appointment import AppointmentOut, AppointmentRegister, AppointmentSchema, GetAppointmentByDoctorIdByUser
from typing import List
from sqlalchemy.orm import aliased
from sqlalchemy import Date

def post_appointment(db: Session, appointment: AppointmentRegister):
    print(appointment)
    
def create_appointment(db: Session, appointment: AppointmentSchema):
    appointment_dict = appointment.model_dump()
    appointment_dict["date"] = datetime.strptime(appointment_dict["date"], "%Y-%m-%d %H:%M:%S")
    appointment_dict["state"] = "PENDIENTE"
    db_appointment = Appointment(**appointment_dict)
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment.__dict__

def get_appointments(db: Session) -> List[Appointment]:
    return db.query(Appointment).all()


def get_appointments_by_user_id(db: Session, user_id: int):
    PatientUser = aliased(User)
    DoctorUser = aliased(User)

    query = (select(
                Appointment.id,
                Appointment.state,
                Appointment.reason,
                Appointment.date,
                PatientUser.name.label("PatientName"),
                DoctorUser.name.label("DoctorName"),
                DoctorUser.id.label("DoctorId"),
                PatientUser.id.label("PatientId"),
                PatientUser.image_url.label("PatientPhoto"),
                DoctorUser.image_url.label("DoctorPhoto"),
                Patient.address,
            )
            .select_from(Appointment)
            .join(DoctorPatients)
            .join(Patient, DoctorPatients.c.patient_id == Patient.id)
            .join(PatientUser, Patient.user_id == PatientUser.id)
            .join(Doctor, DoctorPatients.c.doctor_id == Doctor.id)
            .join(DoctorUser, Doctor.user_id == DoctorUser.id)
            .where(or_(Doctor.user_id == user_id, Patient.user_id == user_id)))
    result = db.execute(query)
    rows = result.fetchall()
    lista: list[GetAppointmentByDoctorIdByUser]  = []
    for row in rows:
        lista.append({
            "id": row.id,
            "state": row.state,
            "reason": row.reason,
            "date": row.date,
            "patient_name": row.PatientName,
            "doctor_name": row.DoctorName,
            "doctor_id": row.DoctorId,
            "patient_id": row.PatientId,
            "patient_photo": row.PatientPhoto,
            "doctor_photo": row.DoctorPhoto,
            "patient_address": row.address
        })
    return lista
