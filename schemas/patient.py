from fastapi import UploadFile
from pydantic import BaseModel
from datetime import date

class PatientOut(BaseModel):
    gender: str
    birthdate: date
    description: str
    address: str
    user_id: int
    familiar_user_id: int

class UserRegister(BaseModel):
    name: str
    lastname: str
    phone: str
    email: str
    cc: str
    password: str
    gender: str
    image_file: UploadFile
    birthdate: date 
    address: str
    description: str
    familiar_name: str
    familiar_lastname: str
    familiar_email: str
    familiar_phone: str