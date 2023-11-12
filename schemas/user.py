from pydantic import BaseModel
from fastapi import UploadFile
from schemas.menu import MenuOut
from typing import List, Optional
from constants.models import DEFAULT_IMG


class User(BaseModel):
    id: int
    name: str
    lastname: str
    email: str
    image_url: str
    rol_id: int


class UserCreate(User):
    password: str


class UserWithMenus(MenuOut):
    menus: List[MenuOut] = []
