from pydantic import BaseModel, ValidationError
from typing import List, Optional


class VitualSignsBase(BaseModel):
    heart_rate: float
    blood_pressure: float
    O2_saturation: float


class VitalSignsCreate(VitualSignsBase):
    pass


class VitalSignsResponse(VitualSignsBase):
    id: int
    patient_id: int
