from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from schemas.user import User, UserCreate, UserGet
from database.db import get_db
from sqlalchemy.orm import Session
from services.user import create_user, exist_user, all_users, put_user, delete_user


router = APIRouter()


@router.post("/create_user", response_model=User)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(user, db) 
    if not new_user:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Error al crear el usuario"}
        )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"data":jsonable_encoder(User(**new_user.__dict__))})


@router.get("/get_all_users", response_model=list[UserGet])
def get_all_users(db: Session = Depends(get_db)):
    users = all_users(db)
    if not users:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"data": users, "message": "No hay usuarios"})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"data": jsonable_encoder(users)})


@router.put("/edit_user/{user_id}", response_model=User)
def edit_user(user_id:int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = put_user(user_id, user, db)
    if db_user is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Usuario no encontrado"})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"data": jsonable_encoder(User(**db_user))})


@router.delete("/delete_user/{user_id}", response_model=User)
def remove_user(user_id:int, db:Session = Depends(get_db)):
    db_user = delete_user(user_id, db)
    if db_user is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Usuario no encontrado", "data": False})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"data": True})
