from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from schemas.email import EmailData, EmailRegisterData
from services.email import send_email_register, send_email_doctor


router = APIRouter()
@router.post("/send_email_register")
def send_register(data: EmailRegisterData):
    response = send_email_register(data)
    if response == "ko":
         return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Error al enviar el email"})
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"message": "Email enviado correctamente"})
        
@router.post("/send_email_doctor_admin")
def send_register_doctor_admin(data: EmailRegisterData):
    response = send_email_doctor(data)
    if response == "ko":
         return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Error al enviar el email"})
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"message": "Email enviado correctamente"})