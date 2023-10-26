from pydantic import BaseModel
from schemas.menu import MenuOut
from typing import List, Optional

class User(BaseModel):
    name: str
    lastname: str
    email: str
    rol_id: int

class UserCreate(User):
    password: str

class UserWithMenus(MenuOut):
    menus: List[MenuOut] = []