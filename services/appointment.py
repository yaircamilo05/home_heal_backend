from datetime import datetime
from sqlalchemy import AliasedReturnsRows, insert, or_, select, text
from sqlalchemy.orm import Session
from models.base import Appointment, Doctor, DoctorPatients, Patient, User
from schemas.appointment import AppointmentRegister, AppointmentSchema, GetAppointmentByDoctorIdByUser, PatientAppointment
from typing import List
from sqlalchemy.orm import aliased
from sqlalchemy import Date

def post_appointment(db: Session, appointment: AppointmentRegister):
    patient = get_patient_by_user_id(db, appointment.user_id)
    date_time_appointment = appointment.date + " " + appointment.hour
    doctor_patients_id = relation_exists(db, appointment.doctor_id, patient.patient_id)
    if(doctor_patients_id != 0):
        appointment_create = AppointmentSchema(reason=appointment.reason, date=date_time_appointment, doctor_patients_id=doctor_patients_id)
        db_appointment_create = create_appointment_function(db, appointment_create)
        return {"data_appointment": db_appointment_create, "data_patient": patient}
    else:
        doctor_patient_id = create_relation_doctor_patient(db, appointment.doctor_id, patient.patient_id)
        appointment_create = AppointmentSchema(reason=appointment.reason, date=date_time_appointment, doctor_patients_id=doctor_patient_id)
        db_appointment_create = create_appointment_function(db, appointment_create)
        return {"data_appointment": db_appointment_create, "data_patient": patient}
        
def get_patient_by_user_id(db: Session, user_id: int) -> PatientAppointment:
    query = text("""select P.id as patient_id, U.name + ' ' + U.lastname as full_name, U.phone, U.cc, U.email, P.address 
        from patients P inner join users U
        on P.user_id = U.id
        where P.user_id = :user_id """)
    
    result = db.execute(query, {"user_id": user_id})
    rows = result.fetchall()
    if len(rows) == 0:
        return None
    return PatientAppointment(patient_id=rows[0].patient_id, full_name=rows[0].full_name, phone=rows[0].phone, cc=rows[0].cc, email=rows[0].email, address=rows[0].address)
            
def create_relation_doctor_patient(db: Session, doctor_id: int, patient_id: int):
    stmt = insert(DoctorPatients).values(doctor_id=doctor_id, patient_id=patient_id).returning(DoctorPatients.c.id)
    result = db.execute(stmt)
    db.commit()
    row = result.fetchone()
    if row is None:
        return None
    return row[0]

def relation_exists(db: Session, doctor_id: int, patient_id: int) -> int:
    query = text("""select id
                    from doctor_patients 
                    where doctor_id = :doctor_id and patient_id = :patient_id""")
    
    result = db.execute(query, {"doctor_id": doctor_id, "patient_id": patient_id})
    rows = result.fetchall()
    if len(rows) == 0:
        return 0
    return rows[0].id
        
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

def get_available_hours_by_date(db: Session, certain_date: str, doctor_id: int):
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
    SELECT DISTINCT FORMAT(A.date, 'HH:mm') AS HoraReservada
	FROM appointments A inner join doctor_patients DP
	ON A.doctor_patients_id = DP.id and DP.doctor_id = :doctor_id
	WHERE CAST(A.date AS DATE) = CAST(:certain_date AS DATE) AND A.state = 'PENDIENTE'
    );
""")
    result = db.execute(query, {"certain_date": certain_date, "doctor_id": doctor_id})
    rows = result.fetchall()
    available_hours: list[str]  = []
    for row in rows:
        available_hours.append(row.Hora)
    return available_hours
