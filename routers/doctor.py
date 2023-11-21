from fastapi import APIRouter, Depends, status
from database.db import get_db
from schemas.doctor import Doctor
from services.doctor import create_doctor, get_doctor_by_user_id
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

router = APIRouter()
@router.get("/get-doctor-by-user_id/{user_id}", response_model=Doctor)
async def getDoctorByUserId(user_id: int, db = Depends(get_db)):
    doctor = get_doctor_by_user_id(user_id, db)
    if doctor is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Doctor not found"})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"data": jsonable_encoder(doctor)})
    