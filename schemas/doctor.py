from pydantic import BaseModel

class Doctor(BaseModel):
    speciality: str
    user_id: int