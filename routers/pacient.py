from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from requests import Session
from database.db import get_db

from schemas.pacient import UserRegister
from services.pacient import register_user


router = APIRouter()

@router.post("/register_user")
def create_new_user(user: UserRegister, db: Session = Depends(get_db)):
    new_user = register_user(user, db)
    if new_user == None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Error al crear el usuario"})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"data": jsonable_encoder(new_user)})