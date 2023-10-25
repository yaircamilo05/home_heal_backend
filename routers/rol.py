from fastapi import APIRouter, Depends

from schemas.rol import RolCreate
from database.db import get_db
from sqlalchemy.orm import Session

from typing import List
from services.rol import create_rol, exist_rol, all_roles


rol_router = APIRouter()


@rol_router.get("/roles", response_model=List[RolCreate])
async def get_roles(db: Session = Depends(get_db)):
    return all_roles(db)