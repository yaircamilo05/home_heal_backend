
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from services import account
from schemas.login import credentials_login
from sqlalchemy.orm import Session
from database.db import get_db
from fastapi import Depends



router = APIRouter()

@router.post('/login', tags=['Account'])
def login(credentials: credentials_login, db: Session = Depends(get_db)):
    token = account.login(credentials,db)
    if token is None:
        return JSONResponse(status_code=404, content={"message": "Usuario no se encontro"})
    print("Token",token)
    return JSONResponse(status_code=200, content={"token": token})

@router.get('/validate_token', tags=['Account'])
def validate_token(token: str):
    token_data = account.validate_token(token)
    if token_data is None:
        return JSONResponse(status_code=404, content={"message": "token invalido"})
    return JSONResponse(status_code=200, content={"token_data": token_data})