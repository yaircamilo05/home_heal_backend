from pydantic import BaseModel
from .user import User

class Doctor(BaseModel):
    speciality: str
    user_id: int

class DoctorWithUser(Doctor):
    user: User