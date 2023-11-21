from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from schemas.email import EmailData
from services.email import send_email


router = APIRouter()
@router.post("/send_email_register")
def send(data: EmailData):
    response = send_email(data)
    print("estoy aqui")
    if response == "ko":
         return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Error al enviar el email"})
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"message": "Email enviado correctamente"})
        
