
from fastapi import APIRouter
from services import account
from schemas.login import credentials_login
from sqlalchemy.orm import Session
from database.db import get_db
from fastapi import Depends



router = APIRouter()

@router.post('/login', tags=['Account'])
def login(credentials: credentials_login, db: Session = Depends(get_db) ):
    tokens = account.login(credentials,db)

@router.get('/validate_token', tags=['Account'])
def validate_token(token: str):
    data_token = account.validate_token(token)
    return data_token