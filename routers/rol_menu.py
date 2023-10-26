from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.db import get_db
from services.rol_menu import add_rol_to_menu, remove_rol_from_menu

router = APIRouter()

@router.post("/{rol_id}/menu/{menu_id}")
async def add_menu_to_rol(rol_id: int, menu_id: int, db: Session = Depends(get_db)):
    if await add_rol_to_menu(db, rol_id, menu_id):
        return {"message": "Menu added to Rol successfully"}
    raise HTTPException(status_code=400, detail="Operation failed")

@router.delete("/{rol_id}/menu/{menu_id}")
async def remove_menu_from_rol(rol_id: int, menu_id: int, db: Session = Depends(get_db)):
    if await remove_rol_from_menu(db, rol_id, menu_id):
        return {"message": "Menu removed from Rol successfully"}
    raise HTTPException(status_code=400, detail="Operation failed")