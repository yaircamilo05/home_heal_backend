from pydantic import BaseModel


class DiagnosisIn(BaseModel):
    description: str
    date: str


class DiagnosisOut(DiagnosisIn):
    id: int
