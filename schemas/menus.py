from pydantic import BaseModel

class MenuCreate(BaseModel):
    title: str
    icon: str

class MenuOut(MenuCreate):
    id: int