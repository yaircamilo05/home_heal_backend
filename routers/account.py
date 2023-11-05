
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from middlewares.guard import NeedToken
from schemas.login import credentials_login
from sqlalchemy.orm import Session
from database.db import get_db
from fastapi import Depends
from services import account


router = APIRouter()


@router.post('/login')
def login(credentials: credentials_login, db: Session = Depends(get_db)):
    token = account.login(credentials, db)
    if token is None:
        return JSONResponse(status_code=404, content={"message": "Usuario no se encontro"})
    return JSONResponse(status_code=200, content={"token": token})


@router.get('/validate_token')
def validate_token(token: HTTPBearer = Depends(NeedToken()), db: Session = Depends(get_db)):
    token_data = account.validate_token(token=token, db=db)
    if token_data is None:
        return JSONResponse(status_code=404, content={"message": "token invalido"})
    return JSONResponse(status_code=200, content={"data": token_data})
