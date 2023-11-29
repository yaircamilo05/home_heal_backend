
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from middlewares.guard import NeedToken
from schemas.login import credentials_login
from sqlalchemy.orm import Session
from database.db import get_db
from fastapi import Depends
from schemas.user import RecoveryPassword
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

@router.post('/recovery_password')
def recovery_password(data: RecoveryPassword, db: Session = Depends(get_db)):
    response = account.recovery_password(data, db)
    if response:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"data": response})
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"data": response})

@router.post('change_password')
def change_password(token: str, password: str, db: Session = Depends(get_db)):
    response = account.change_password(token, password, db)
    if response:
        return JSONResponse(status_code=404, content={"data": response})
    return JSONResponse(status_code=200, content={"data": response})