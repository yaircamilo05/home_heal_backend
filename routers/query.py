from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from database.db import get_db
from schemas.cares import GeneratedCare


from sqlalchemy.orm import Session
from services.query import vi_searcher


router = APIRouter()


# Endpoint y clave secreta del servicio de diagnóstico
HEALTH_BOT_ENDPOINT = 'https://bot-api-eastus.healthbot.microsoft.com/api/tenants/health-i-aemela6/diagnose'
HEALTH_BOT_SECRET = '6oG8Q~Mj25XWuoSe-qK5avEryTumaWNFvScR1c~L'


@router.get(
    "/generate-cares/{patient_id}/{user_id}",
    summary="Search the best diagnosis based on the patient actual vital signs (ia implementation)."
)
async def generate_care(patient_id: int, user_id: int, db: Session = Depends(get_db)):
    result = vi_searcher(patient_id, user_id, db)
    # obtained_cares: list[GeneratedCare] = vi_searcher(patient_id, db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cares weren't generated"
        )
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={'data': jsonable_encoder(result)}
    )
