from pydantic import BaseModel
from datetime import datetime


class VitalSignsRequest(BaseModel):
    O2_saturation: float
    blood_pressure: float
    hearth_rate: float


class VitalSignsCreate(VitalSignsRequest):
    pass


class VitalSignsUpdate(VitalSignsRequest):
    pass


class VitalSignsResponse(VitalSignsRequest):
    id: int

    patient_id: int
