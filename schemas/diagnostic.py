from pydantic import BaseModel


class DiagnosticCreate(BaseModel):
    description: str 
    patient_id: int
    doctor_id: int

