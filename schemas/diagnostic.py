from pydantic import BaseModel, ValidationError
from typing import List, Optional


class DiagnosisRequest(BaseModel):
    description: str


class DiagnosisCreate(DiagnosisRequest):
    doctor_patients_id: int
    patient_id: int


class DiagnosisReplace(DiagnosisRequest):
    pass


class DiagnosisResult(DiagnosisRequest):
    id: int
    doctor_patients_id: int
    patient_id: int
from pydantic import BaseModel


class DiagnosticCreate(BaseModel):
    description: str 
    patient_id: int
    doctor_id: int

