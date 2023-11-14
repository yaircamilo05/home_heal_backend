from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from database.db import get_db
from schemas.rol_menus import RolMenuIds
from services.rol_menu import add_role_menu, remove_role_menu, get_menus_role

router = APIRouter()


@router.post("/asign_menu_to_role")
def add_menu_to_rol(ids:RolMenuIds, db: Session = Depends(get_db)):
    data = add_role_menu(db, ids.rol_id, ids.menu_id)
    if data is None:
       return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Menu already assigned to Rol"})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"data": jsonable_encoder(data)})


@router.get("/menus/{rol_id}")
def get_menus_by_role(rol_id: int, db: Session = Depends(get_db)):
    menus = get_menus_role(db, rol_id)
    if menus:
        return menus
    raise HTTPException(status_code=404, detail="Menus not found")


@router.delete("/delete_menu_to_role/{rol_id}/{menu_id}")
def remove_menu_from_rol(rol_id: int, menu_id: int, db: Session = Depends(get_db)):
    if remove_role_menu(db, rol_id, menu_id):
        return {"message": "Menu removed from Rol successfully"}
    raise HTTPException(status_code=400, detail="Operation failed")
