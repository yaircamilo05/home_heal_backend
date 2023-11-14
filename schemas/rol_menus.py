from typing import List
from .rol import RolBase, RolOut
from .menu import MenuOut, MenuOut
from pydantic import BaseModel

class RolWithMenus(RolOut):
    menus: List[MenuOut] = []

class MenuWithRoles(MenuOut):
    roles: List[RolBase] = []

class RolMenuSchema(BaseModel):
    rol: RolWithMenus
    menu: MenuWithRoles

class RolMenuIds(BaseModel):
    rol_id: int
    menu_id: int