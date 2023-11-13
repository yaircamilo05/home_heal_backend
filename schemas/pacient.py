from pydantic import BaseModel
from sqlalchemy import Date

class PacientOut(BaseModel):
    gender: str
    date_of_birth: Date
    description: str
    lastname: str
    address: str
    user_id: int
    familiar_user_id: int    

class UserRegister(BaseModel):
    name: str
    latname: str
    phone: str
    email: str
    CC: str
    password: str
    gender: str
    image_url: str
    date_of_birth: Date
    address: str
    description: str
    familiar_name: str
    familiar_lastname: str
    familiar_email: str
    familiar_phone: str
    