from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from database.db import get_db
from schemas.vital_signs import (
    VitalSignsResponse, VitalSignsCreate, VitalSignsUpdate
)
from services.vital_signs import (
    create_vital_sign, remove_vital_sign, read_vital_sign,
    read_vital_signs, replace_vital_signs, read_vital_signs
)

router = APIRouter()


@router.get('/vital_signs/', response_model=List[VitalSignsResponse])
async def get_vital_signs(db: Session = Depends(get_db)):
    vital_sign, code = read_vital_signs(db)
    if code == status.HTTP_204_NO_CONTENT:
        raise HTTPException(
            status_code=code,
            detail=f'There are no vital signs registered: {vital_sign}'
        )
    if code == status.HTTP_404_NOT_FOUND:
        raise HTTPException(
            status_code=code,
            detail=f'Patient not found: {vital_sign}'
        )
    return JSONResponse(
        status_code=code,
        content={'data': jsonable_encoder(vital_sign)},
    )


@router.post('/vital_signs/', response_model=VitalSignsResponse)
async def post_vital_sign(patient_id: int, vital_sign: VitalSignsCreate, db: Session = Depends(get_db)):
    vital_sign_created, code = create_vital_sign(db, patient_id, vital_sign)
    if code == status.HTTP_404_NOT_FOUND:
        raise HTTPException(
            status_code=code,
            detail=f'Patient not found: {vital_sign_created}'
        )
    return JSONResponse(
        status_code=code,
        content={'data': jsonable_encoder(vital_sign_created)},
    )


@router.get('/vital_signs/{vital_sign_id}', response_model=VitalSignsResponse)
async def get_vital_sign(vital_sign_id: int, db: Session = Depends(get_db)):
    vital_sign, code = read_vital_sign(db, vital_sign_id)
    if code == status.HTTP_404_NOT_FOUND:
        raise HTTPException(
            status_code=code,
            detail=f'Patient not found: {vital_sign}'
        )
    return JSONResponse(
        status_code=code,
        content={'data': jsonable_encoder(vital_sign)},
    )


@router.put('/vital_signs/{patient_id}', response_model=VitalSignsResponse)
async def put_vital_sign(patient_id: int, vital_sign: VitalSignsUpdate, db: Session = Depends(get_db)):
    vital_sign_updated, code = replace_vital_signs(db, patient_id, vital_sign)
    if code == status.HTTP_404_NOT_FOUND:
        raise HTTPException(
            status_code=code,
            detail=f'Patient not found: {vital_sign_updated}'
        )
    return JSONResponse(
        status_code=code,
        content={'data': jsonable_encoder(vital_sign_updated)},
    )


@router.delete('/vital_signs/{vital_sign_id}')
async def delete_vital_sign(vital_sign_id: int, db: Session = Depends(get_db)):
    _, code = remove_vital_sign(db, vital_sign_id)
    if code == status.HTTP_404_NOT_FOUND:
        return JSONResponse(
            status_code=code,
            content={'data': jsonable_encoder(False)}
        )
    return JSONResponse(
        status_code=code,
        content={'data': jsonable_encoder(True)},
    )
