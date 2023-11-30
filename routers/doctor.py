from fastapi import APIRouter, Depends, status
from database.db import get_db
from schemas.doctor import DoctorBase, DoctorCreate
from services.doctor import create_doctor, get_doctor_by_user_id
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

router = APIRouter()
@router.get("/get_doctor_by_user_id/{user_id}")
async def getDoctorByUserId(user_id: int, db = Depends(get_db)):
    doctor = get_doctor_by_user_id(user_id, db)
    if doctor is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Doctor not found"})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"data": jsonable_encoder(doctor)})

@router.post("/create_doctor")
async def createDoctor(doctor: DoctorCreate, db = Depends(get_db)):
    new_doctor = create_doctor(doctor, db)
    if new_doctor is None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Error al crear el doctor"})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"data": jsonable_encoder(new_doctor)})