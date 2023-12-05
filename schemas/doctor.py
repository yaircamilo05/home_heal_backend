from pydantic import BaseModel
from .user import User

class DoctorBase(BaseModel):
    speciality: str
    user_id: int

class DoctorOut(BaseModel):
    id: int
    full_name: str
    phone: str
    cc: str
    email: str
    
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

class DoctorWithUser(DoctorBase):
    user: User

