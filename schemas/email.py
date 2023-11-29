from pydantic import BaseModel

class EmailData(BaseModel):
    hash: str
    to_destination: str
    name: str
    
class EmailRegisterData(EmailData):
    password: str

class EmailVitalSignsData(BaseModel):
    hash: str
    to_destination: list[str] 
    name: str
    subject: str
    relationship: str
    date: str
    name_editor: str
    name_patient: str
    hearth_rate: int
    state_hearth_rate: str
    color_hearth_rate: str
    blood_pressure: str
    state_blood_pressure: str
    color_blood_pressure: str
    o2_saturation: int
    state_o2_saturation: str
    color_o2_saturation: str

class EmailLinkData(EmailData):
    link: str


    