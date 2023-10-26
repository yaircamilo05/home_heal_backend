from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.db import get_db
from services.rol_menu import add_rol_menu, remove_rol_menu, get_menus_role

router = APIRouter()

@router.post("/rol/{rol_id}/menu/{menu_id}")
async def add_menu_to_rol(rol_id: int, menu_id: int, db: Session = Depends(get_db)):
    if await add_rol_menu(db, rol_id, menu_id):
        return {"message": "Menu added to Rol successfully"}
    raise HTTPException(status_code=400, detail="Operation failed")

@router.get("/menus/{rol_id}")
async def get_menus_by_role(rol_id: int, db: Session = Depends(get_db)):
    return await get_menus_role(db, rol_id)

@router.delete("/rol/{rol_id}/menu/{menu_id}")
async def remove_menu_from_rol(rol_id: int, menu_id: int, db: Session = Depends(get_db)):
    if await remove_rol_menu(db, rol_id, menu_id):
        return {"message": "Menu removed from Rol successfully"}
    raise HTTPException(status_code=400, detail="Operation failed")

