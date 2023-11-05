from fastapi import APIRouter, Depends, HTTPException

from database.db import get_db
from sqlalchemy.orm import Session
from middlewares.guard import SuperAdmin
from schemas.rol import RolSchema, RolOut, RolWithMenus
from typing import List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from services.rol import get_roles_with_menus, post_rol, exist_rol, get_roles, get_role, put_rol, delete_rol

router = APIRouter()


@router.post('/role')
async def create_rol(rol: RolSchema,db: Session = Depends(get_db)):
    return post_rol(rol, db)


@router.get('/roles', response_model=List[RolOut])
async def read_roles(db: Session = Depends(get_db)):
    return get_roles(db)

@router.get('/roles_with_menus', response_model=List[RolWithMenus])
async def read_roles(db: Session = Depends(get_db)):
    roles_with_menus =  get_roles_with_menus(db)
    if roles_with_menus is None:
        raise HTTPException(
            status_code=404, detail=f'Rol not found'
        )
    return JSONResponse(status_code=200, content={ "data":jsonable_encoder(roles_with_menus)})


@router.get('/role/{id}', response_model=RolOut)
async def read_rol(id: int, db: Session = Depends(get_db)):
    if not exist_rol(id, db):
        raise HTTPException(
            status_code=404, detail=f'Rol {id} not found'
        )
    return JSONResponse(
        status_code=200, content=jsonable_encoder(get_role(id, db))
    )


@router.put('/role/{id}', response_model=RolSchema)
async def update_role(id: int, rol: RolSchema, db: Session = Depends(get_db)):
    if not exist_rol(id, db):
        raise HTTPException(
            status_code=404, detail=f'Rol {id} not found'
        )
    rol_updated = put_rol(id, rol, db)
    return JSONResponse(
        status_code=200, content=jsonable_encoder(rol_updated)
    )


@router.delete('/role/{id}', response_model=int)
async def remove_role(id: int, db: Session = Depends(get_db)):
    if not exist_rol(id, db):
        raise HTTPException(
            status_code=404, detail=f'Rol {id} not found'
        )
    deleted = delete_rol
    return JSONResponse(
        status_code=200, content=jsonable_encoder(deleted)
    )
