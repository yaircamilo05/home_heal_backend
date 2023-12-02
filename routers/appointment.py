from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.appointment import AppointmentOut, AppointmentSchema, GetAppointmentByDoctorIdByUser
from services.appointment import get_appointments, get_appointments_by_user_id, create_appointment_function, get_available_hours_by_date, patch_appointment_state
from typing import List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()

@router.get("/get_available_hours/{certain_date}", response_model=List[str])
def get_available_hours(certain_date: str, db: Session = Depends(get_db)):
    db_hours = get_available_hours_by_date(db, certain_date)
    if db_hours is None:
        raise HTTPException(status_code=404, detail="There are no times available for the date")
    return JSONResponse(status_code=200, content=jsonable_encoder({"data": db_hours}))

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
    schemaAppointment = create_appointment_function(db, appointment)
    if schemaAppointment is None:
        raise HTTPException(status_code=404, detail="Appointment already exists")
    return JSONResponse(status_code=200, content=jsonable_encoder({"data": schemaAppointment}))

@router.patch("/update_appointment_state/{idAppointment}/{state}")
def update_appointment(idAppointment:int , state:int,db: Session = Depends(get_db)):
    schemaAppointment = patch_appointment_state(db, idAppointment,state)
    if schemaAppointment is None:
        raise HTTPException(status_code=404, detail="Appointment already exists")
    return JSONResponse(status_code=200, content=jsonable_encoder({"data": schemaAppointment}))