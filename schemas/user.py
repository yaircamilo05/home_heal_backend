from pydantic import BaseModel

class User(BaseModel):
    name: str
    lastname: str
    email: str
    rol_id: int
    #menus: list[Menus]

class UserCreate(User):
    password: str