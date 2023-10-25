from fastapi import APIRouter, Depends

from database.db import get_db
from sqlalchemy.orm import Session
# from schemas.rol import RolCreate, RolOut

from typing import List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
# from services.rol import post_rol, exist_rol, get_roles, get_role, put_rol, delete_rol

router = APIRouter()