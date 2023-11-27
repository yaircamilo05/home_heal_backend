from pydantic import BaseModel
from fastapi import UploadFile
from schemas.menu import MenuOut
from schemas.rol import RolOut
from typing import List, Optional
from constants.models import DEFAULT_IMG


class User(BaseModel):
    ##id: int
    name: str
    lastname: str
    email: str
    image_url: str
    rol_id: int
    cc: str
    phone: str


class UserCreate(User):
    password: str
    specialty: str


class UserWithMenus(MenuOut):
    menus: List[MenuOut] = []


class UserGet(BaseModel):
    id: int
    name: str
    lastname: str
    email: str
    image_url: str
    rol: RolOut
    cc: str
    phone: str
    specialty: str

class UserGetLogin(BaseModel):
    id: int
    name: str
    lastname: str
    email: str
    image_url: str
    rol_id: int
    cc: str
    phone: str


class UserAux(BaseModel):
    name: str
    lastname: str
    email: str
    image_url: str
    rol_id: int
    cc: str
    phone: str
    password: str


class UserUpdate(User):
    specialty: str