from pydantic import BaseModel
from schemas.menu import MenuOut
from typing import List, Optional
from constants.models import DEFAULT_IMG


class User(BaseModel):
    name: str
    lastname: str
    email: str
    file_img: Optional[str]
    rol_id: int


class UserCreate(User):
    password: str


class UserWithMenus(MenuOut):
    menus: List[MenuOut] = []
