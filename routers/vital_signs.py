from fastapi import APIRouter, Depends,status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pytest import Session
from database.db import get_db
from services.vital_signs import get_history_vital_signs_patient, get_vital_signs_patient


router = APIRouter()

@router.get("/get_vital_signs_history/{patient_id}")
def get_vital_signs_history(patient_id: int, db: Session = Depends(get_db)):
    vital_signs_history = get_history_vital_signs_patient(patient_id,db)
    if vital_signs_history is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"data": jsonable_encoder(vital_signs_history)})
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "No se encontraron registros de signos vitales para el paciente"})

@router.get("/get_last_vital_signs/{patient_id}")
def get_vital_signs_initiated(patient_id: int, db: Session = Depends(get_db)):
    vital_signs  = get_vital_signs_patient(patient_id,db)
    if vital_signs is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"data": jsonable_encoder(vital_signs)})
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"data": None })