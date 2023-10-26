from pydantic import BaseModel
from typing import List, Optional


class MenuSchema(BaseModel):
    title: str
    icon: str
    link: str


class MenuOut(MenuSchema):
    id: int

    class Config:
        orm_mode = True

# class MenuBase(BaseModel):
#     title: str
#     icon: Optional[str] = None

# class MenuCreate(MenuBase):
#     pass

# class MenuUpdate(BaseModel):
#     title: Optional[str] = None
#     icon: Optional[str] = None
#     rol_ids: Optional[List[int]] = None

# class MenuInDBBase(MenuBase):
#     id: int

#     class Config:
#         orm_mode = True

# class Menu(MenuInDBBase):
#     roles: List['Rol'] = []
