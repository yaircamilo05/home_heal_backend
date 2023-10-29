from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from database.db import get_db
from middlewares.guard import SuperAdmin
from schemas.rol import RolCreate, RolUpdate, RolSchema
from services.rol import (
    post_rol, get_roles, get_role, put_rol, delete_rol, exist_rol_id, exist_rol_name
)


router = APIRouter(dependencies=[Depends(SuperAdmin())])


@router.post('/role', response_model=RolSchema, status_code=status.HTTP_201_CREATED)
async def create_rol(rol: RolCreate, db: Session = Depends(get_db)):
    if exist_rol_name(rol.name, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Rol {rol.name} already exist'
        )
    rol_created = post_rol(rol, db)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(rol_created)
    )


@router.get('/roles', response_model=List[RolSchema], status_code=status.HTTP_302_FOUND)
async def read_roles(db: Session = Depends(get_db)):
    roles = get_roles(db)
    print(roles)
    if not roles:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            headers={'X-Error': f'There are no found roles: {jsonable_encoder(roles)}'}
        )
    return JSONResponse(
        status_code=status.HTTP_302_FOUND,
        content=jsonable_encoder(roles)
    )


@router.get('/role/{id}', response_model=RolSchema, status_code=status.HTTP_302_FOUND)
async def read_rol(id: int, db: Session = Depends(get_db)):
    if not exist_rol_id(id, db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Rol {id} was not found'
        )
    rol: RolSchema = get_role(id, db)
    return JSONResponse(
        status_code=status.HTTP_302_FOUND,
        content=jsonable_encoder(rol)
    )


@router.put('/role/{id}', response_model=RolSchema, status_code=status.HTTP_302_FOUND)
async def update_role(id: int, rol: RolUpdate, db: Session = Depends(get_db)):
    if not exist_rol_id(id, db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Rol {id} was not found'
        )
    rol_updated: RolSchema = put_rol(id, rol, db)
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content=jsonable_encoder(rol_updated)
    )


@router.delete('/role/{id}', response_model=RolSchema, status_code=status.HTTP_302_FOUND)
async def remove_role(id: int, db: Session = Depends(get_db)):
    if not exist_rol_id(id, db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Rol {id} was not found'
        )
    rol_removed: RolSchema = delete_rol(id, db)
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content=jsonable_encoder(rol_removed)
    )
