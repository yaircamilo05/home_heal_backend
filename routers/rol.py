from fastapi import APIRouter, Depends

from database.db import get_db
from sqlalchemy.orm import Session
from schemas.rol import RolCreate, RolOut

from typing import List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from services.rol import post_rol, exist_rol, get_roles, get_role, put_rol, delete_rol

router = APIRouter()


@router.post('/role', response_model=RolCreate, tags=['Rol'])
async def create_rol(rol: RolCreate, db: Session = Depends(get_db)):
    return post_rol(rol, db)


@router.get('/roles', response_model=List[RolOut], tags=['Rol'])
async def read_roles(db: Session = Depends(get_db)):
    return get_roles(db)


@router.get('/role/{id}', response_model=RolOut, tags=['Rol'])
async def read_rol(id: int, db: Session = Depends(get_db)):
    if not exist_rol(id, db):
        return JSONResponse(
            status_code=404, content={'message': f'Rol {id} not found'}
        )
    return JSONResponse(
        status_code=200, content=jsonable_encoder(get_role(id, db))
    )


@router.put('/role/{id}', response_model=RolCreate, tags=['Rol'])
async def update_role(id: int, rol: RolCreate, db: Session = Depends(get_db)):
    if not exist_rol(id, db):
        return JSONResponse(
            status_code=404, content={'message': f'Rol {id} not found'}
        )
    rol_updated = put_rol(id, rol, db)
    return JSONResponse(
        status_code=200, content=jsonable_encoder(rol_updated)
    )


@router.delete('/role/{id}', response_model=int, tags=['Rol'])
async def remove_role(id: int, db: Session = Depends(get_db)):
    if not exist_rol(id, db):
        return JSONResponse(
            status_code=404, content={'message': f'Rol {id} not found'}
        )
    deleted: int = delete_rol(id, db)
    return JSONResponse(
        status_code=200, content={'message': f'Rol {id} deleted'}
    )
