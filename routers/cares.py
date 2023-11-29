from fastapi import APIRouter, Depends, status
from database.db import get_db
from schemas.cares import CaresGet, CaresCreate
from services.cares import create_care, get_cares_by_patient_id, delete_care
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/create-care", response_model=CaresCreate)
async def createCare(care: CaresCreate, db = Depends(get_db)):
    care = create_care(care, db)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"data": jsonable_encoder(care)})


@router.get("/get-cares-by-patient-id/{patient_id}", response_model=list[CaresGet])
async def getCaresByPatientId(patient_id: int, db = Depends(get_db)):
    cares = get_cares_by_patient_id(patient_id, db)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"data": jsonable_encoder(cares)})


@router.delete("/delete-care/{id}", response_model=bool)
async def deleteCare(id: int, db = Depends(get_db)):
    care = delete_care(id, db)
    if care is False:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Care not found"})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"data": jsonable_encoder(care)})