from pydantic import BaseModel


class RolCreate(BaseModel):
    name: str
    description: str


class RolOut(RolCreate):
    id: int
