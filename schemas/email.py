from pydantic import BaseModel

class EmailData(BaseModel):
    hash: str
    to_destination: str
    
class EmailRegisterData(EmailData):
    name: str
    password: str