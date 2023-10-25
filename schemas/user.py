from pydantic import BaseModel

class User(BaseModel):
    name: str
    lastname: str
    email: str
    rol_id: int

class UserCreate(User):
    password: str