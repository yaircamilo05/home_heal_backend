from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from schemas.user import User, UserCreate
from database.db import get_db
from sqlalchemy.orm import Session
from services.user import create_user, exist_user, all_users


router = APIRouter()


@router.post("/create_user")
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(user, db)
    if not new_user:
        return JSONResponse(
            status_code=400, content={"message": "Error al crear el usuario"}
        )
    return User(**new_user.__dict__)


@router.get("/all_users")
def get_all_users(db: Session = Depends(get_db)):
    users = all_users(db)
    if not users:
        return JSONResponse(
            status_code=404, content={"message": "No hay usuarios"}
            )
    return users
