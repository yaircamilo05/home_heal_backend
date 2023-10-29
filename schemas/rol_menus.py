from typing import List, Optional
from .rol import RolBase
from .menu import MenuOut, MenuOut
from pydantic import BaseModel

class RolWithMenus(RolBase):
    menus: List[MenuOut] = []

class MenuWithRoles(MenuOut):
    roles: List[RolBase] = []

class RolMenuSchema(BaseModel):
    rol: RolWithMenus
    menu: MenuWithRoles