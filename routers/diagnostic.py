from fastapi import APIRouter, Depends, status
from database.db import get_db
from schemas.diagnostic import DiagnosticCreate
from services.diagnostic import create_diagnostic, get_diagnostic_by_patient_id, delete_diagnostic
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/create-diagnostic")
async def createDiagnostic(diagnostic: DiagnosticCreate, db = Depends(get_db)):
    diagnostic_bd = create_diagnostic(diagnostic, db)
    if diagnostic_bd is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "doctor_patient not found"})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"data": jsonable_encoder(diagnostic_bd)})


@router.get("/get-diagnostic-by-patient-id/{patient_id}")
async def getDiagnosticByPatientId(patient_id: int, db = Depends(get_db)):
    diagnostics = get_diagnostic_by_patient_id(patient_id, db)
    if not diagnostics:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Cares not found"})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"data": jsonable_encoder(diagnostics)})


@router.delete("/delete-diagnostic/{id}", response_model=bool)
async def deleteDiagnostic(id: int, db = Depends(get_db)):
    diagnostic = delete_diagnostic(id, db)
    if diagnostic is False:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Care not found"})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"data": jsonable_encoder(diagnostic)})
