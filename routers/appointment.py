from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.appointment import AppointmentOut, AppointmentSchema, GetAppointmentByDoctorIdByUser
from services.appointment import get_appointments, get_appointments_by_user_id, create_appointment
from typing import List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()

@router.get("/get_all_appointments",response_model=List[AppointmentOut])
def read_appointments(db: Session = Depends(get_db)):
    db_appointments = get_appointments(db)
    if db_appointments is None:
        raise HTTPException(status_code=404, detail="Appointments not found")
    return JSONResponse(status_code=200, content=jsonable_encoder({"data": db_appointments}))

@router.get("/get_appointments_by_userId/{userId}",response_model=List[GetAppointmentByDoctorIdByUser])
def read_appointments_by_doctor_patient_id(userId: int, db: Session = Depends(get_db)):
    db_appointments = get_appointments_by_user_id(db, userId)
    if db_appointments is None:
        raise HTTPException(status_code=404, detail="Appointments not found")
    return JSONResponse(status_code=200, content=jsonable_encoder({"data": db_appointments}))

@router.post("/post_appointments")
def create_appointment(appointment: AppointmentSchema, db: Session = Depends(get_db)):
    schemaAppointment = create_appointment(db, appointment)
    if schemaAppointment is None:
        raise HTTPException(status_code=404, detail="Appointment already exists")
    return JSONResponse(status_code=200, content=jsonable_encoder({"data": schemaAppointment}))
