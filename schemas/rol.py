from pydantic import BaseModel
from typing import List, Optional

# from pydantic import BaseModel
# from typing import Optional


class RolSchema(BaseModel):
    name: str
    description:str 


class RolOut(RolSchema):
    id: int

    class Config:
        orm_mode = True
