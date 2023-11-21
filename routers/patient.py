import json
from fastapi import APIRouter, Body, Depends, Form, UploadFile, status, File
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import parse_obj_as
from requests import Session
from database.db import get_db

from schemas.patient import UserRegister, PatientOut
from services.patient import all_patients, register_user


router = APIRouter()

def parse_user(user: str = Body(...)):
    return parse_obj_as(UserRegister, json.loads(user))

@router.post("/register_user")
def register_patient_user(user: UserRegister = Depends(parse_user), image_file: UploadFile = File(...), db: Session = Depends(get_db)):
    print('estoy aqui')
    new_patient = register_user(user,image_file, db)
    if new_patient == None:
         return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Error al registrar el usuario"})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"data": jsonable_encoder(user)})

@router.get("/get_all_patients")
def get_all_patients(db: Session = Depends(get_db)):
    patients = all_patients(db)
    if not patients:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"data": patients, "message": "No hay pacientes"})
    return  JSONResponse(status_code=status.HTTP_201_CREATED, content={"data":jsonable_encoder(patients)})
