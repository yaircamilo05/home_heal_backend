from pydantic import BaseModel
from .doctor import DoctorWithUser


class Care(BaseModel):
    id: int
    description: str
    doctor_patient_id: int


class CaresGet(BaseModel):
    id: int
    description: str
    doctor_patient_id: int
    doctor: DoctorWithUser


class CaresCreate(BaseModel):
    description: str
    patient_id: int
    doctor_id: int


class GeneratedCare(CaresCreate):
    title: str
