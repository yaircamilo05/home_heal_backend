from pydantic import BaseModel

class credentials_login(BaseModel):
    email: str
    password: str