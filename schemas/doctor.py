from pydantic import BaseModel
from .user import User

class DoctorBase(BaseModel):
    speciality: str
    user_id: int

class DoctorCreate(BaseModel):
    name: str
    lastname: str
    email: str
    image_url: str
    rol_id: int
    cc: str
    phone: str
    password: str
    specialty: str

