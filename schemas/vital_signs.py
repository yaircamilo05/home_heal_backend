from pydantic import BaseModel, ValidationError
from typing import List, Optional


class VitualSignsBase(BaseModel):
    heart_rate: int
    blood_pressure: int
    O2_saturation: int


class VitalSignsCreate(VitualSignsBase):
    pass


class VitalSignsResponse(VitualSignsBase):
    id: int
    patient_id: int
