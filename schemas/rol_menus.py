from typing import List, Optional
from .rol import RolSchema
from .menu import MenuOut, MenuOut
from pydantic import BaseModel

class RolWithMenus(RolSchema):
    menus: List[MenuOut] = []

class MenuWithRoles(MenuOut):
    roles: List[RolSchema] = []

class RolMenuSchema(BaseModel):
    rol: RolWithMenus
    menu: MenuWithRoles