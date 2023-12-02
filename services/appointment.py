from datetime import datetime
from sqlalchemy import AliasedReturnsRows, or_, select, text
from sqlalchemy.orm import Session
from models.base import Appointment, Doctor, DoctorPatients, Patient, User
from schemas.appointment import AppointmentOut, AppointmentRegister, AppointmentSchema, GetAppointmentByDoctorIdByUser
from typing import List
from sqlalchemy.orm import aliased
from sqlalchemy import Date

def post_appointment(db: Session, appointment: AppointmentRegister):
    print(appointment)
    
def create_appointment_function(db: Session, appointment: AppointmentSchema):
    appointment_dict = appointment.model_dump()
    appointment_dict["date"] = datetime.strptime(appointment_dict["date"], "%Y-%m-%d %H:%M")
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
                PatientUser.email.label("PatientEmail"),
                DoctorUser.email.label("DoctorEmail")
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
            "patient_address": row.address,
            "patient_email": row.PatientEmail,
            "doctor_email": row.DoctorEmail
        })
    return lista

def patch_appointment_state(db: Session, appointment_id: int, state: int):
    AppointmentDb = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if AppointmentDb is None:
        return None
    if AppointmentDb.date < datetime.now() and state == 1:
        AppointmentDb.state = "REALIZADA"
    elif AppointmentDb.date > datetime.now() and state == 2:
        AppointmentDb.state = "CANCELADA"
    else:
        raise Exception("No se puede cambiar el estado de la cita")
    db.commit()
    db.refresh(AppointmentDb)
    return AppointmentDb.__dict__

def get_available_hours_by_date(db: Session, certain_date: str):
    query = text("""
    WITH HorasDisponibles AS (
        SELECT '07:00' AS Hora
        UNION SELECT '08:00' UNION SELECT '09:00' 
        UNION SELECT '10:00' UNION SELECT '11:00' 
        UNION SELECT '12:00' UNION SELECT '13:00' 
        UNION SELECT '14:00' UNION SELECT '15:00' 
        UNION SELECT '16:00' UNION SELECT '17:00'
    )
    SELECT Hora
    FROM HorasDisponibles
    WHERE Hora NOT IN (
        SELECT FORMAT(date, 'HH:mm') AS HoraReservada
        FROM appointments
        WHERE CAST(date AS DATE) = CAST(:certain_date AS DATE) AND state = 'PENDIENTE'
    );
""")
    result = db.execute(query, {"certain_date": certain_date})
    rows = result.fetchall()
    available_hours: list[str]  = []
    for row in rows:
        available_hours.append(row.Hora)
    return available_hours
