from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import Date

class AppointmentSchema(BaseModel):
    reason: str
    date: str
    doctor_patients_id: int
    
class AppointmentRegister(BaseModel):
    reason: str
    date: str
    speciality: str
    
class AppointmentOut(AppointmentSchema):
    id: int

    class Config:
        orm_mode = True

class AppointmentSchemaIn(AppointmentSchema):
    def model_dump(self):
        return {
            "reason": self.reason,
            "date": self.date,
            "status": self.status,
            "doctor_patient_id": self.doctor_patient_id
        }
    
class GetAppointmentByDoctorIdByUser(BaseModel):
    id: int
    reason: str
    date: str
    state: str
    doctor_name: str
    patient_name: str
    doctor_id: int
    patient_id: int
    patient_photo: str
    doctor_photo: str
    patient_address: str

    class Config:
        orm_mode = True