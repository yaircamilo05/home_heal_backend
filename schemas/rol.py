from pydantic import BaseModel, ValidationError
from typing import List, Optional

from pydantic import BaseModel, Field
from typing import Optional


class RolBase(BaseModel):
    name: str
    description:str 


class RolCreate(RolBase):
    pass


class RolUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]


class RolSchema(RolBase):
    id: int

    # class Config:
    #     orm_mode = True
    #     from_attributes = True
