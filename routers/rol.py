from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from database.db import get_db
from middlewares.guard import SuperAdmin
from schemas.rol import RolCreate, RolUpdate, RolOut
from services.rol import (
    post_rol, get_roles, get_role, put_rol, delete_rol
)


router = APIRouter()


@router.post('/role', response_model=RolOut)
async def create_rol(rol: RolCreate, db: Session = Depends(get_db)):
    rol_created: RolOut = post_rol(rol, db)
    if rol_created is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Rol {rol.name} already exists'
        )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'data': jsonable_encoder(rol_created)}
    )


@router.get('/roles', response_model=List[RolOut])
async def read_roles(db: Session = Depends(get_db)):
    roles: RolOut = get_roles(db)
    if not roles:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            headers={
                'X-Error': f'There are no found roles: {jsonable_encoder(roles)}'
            }
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'data': jsonable_encoder(roles)}
    )


@router.get('/role/{id}', response_model=RolOut)
async def read_rol(id: int, db: Session = Depends(get_db)):
    rol: RolOut = get_role(id, db)
    if rol is None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            headers={
                'X-Error': f'Rol {id} was not found'
            }
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'data': jsonable_encoder(rol)}
    )


@router.put('/role/{id}', response_model=RolOut)
async def update_role(id: int, rol: RolUpdate, db: Session = Depends(get_db)):
    rol_updated: RolOut = put_rol(id, rol, db)
    if rol_updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Rol {id} was not found'
        )

    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={'data': jsonable_encoder(rol_updated)}
    )


@router.delete('/role/{id}')
async def remove_role(id: int, db: Session = Depends(get_db)) -> bool:
    rol_removed: RolOut = delete_rol(id, db)
    if rol_removed:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={'data': True}
        )
    raise JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={'data': False}
    )
