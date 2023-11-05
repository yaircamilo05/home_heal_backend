from pydantic import BaseModel
from typing import List, Optional

from schemas.menu import MenuOut

# from pydantic import BaseModel
# from typing import Optional


class RolSchema(BaseModel):
    name: str
    description:str 

class RolWithMenus(RolSchema):
    id: int
    menus: List[MenuOut]

class RolOut(RolSchema):
    id: int

    class Config:
        orm_mode = True
