from pydantic import BaseModel

class RolCreate(BaseModel):
    name: str

class RolOut(BaseModel):
    id: int