from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from schemas.email import EmailAppointmentData, EmailCancelData, EmailData, EmailLinkData, EmailRegisterData, EmailVitalSignsData
from services.email import send_email_appointment_cancellation, send_email_appointment_confirmation, send_email_register, send_email_doctor_admin, send_email_vital_signs, send_link_email_recory_password


router = APIRouter()
@router.post("/send_email_register")
def send_register_email(data: EmailRegisterData):
    response = send_email_register(data)
    if response == "ko":
         return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Error al enviar el email"})
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"message": "Email enviado correctamente"})
        
@router.post("/send_email_doctor_admin")
def send_register_doctor_admin_email(data: EmailRegisterData):
    response = send_email_doctor_admin(data)
    if response == "ko":
         return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Error al enviar el email"})
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"message": "Email enviado correctamente"})

@router.post("/send_email_vital_signs")
def send_vital_signs_email(data: EmailVitalSignsData):
    response = send_email_vital_signs(data)
    if response == "ko":
         return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Error al enviar el email"})
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"message": "Email enviado correctamente"})

@router.post('/send_email_recovery_password')
def send_recovery_password_email(data:EmailLinkData):
    response = send_link_email_recory_password(data)
    if response == "ko":
         return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Error al enviar el email"})
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"message": "Email enviado correctamente"})

@router.post("/send_email_appointment_cancellation")
def send_appointment_cancellation_email(data: EmailCancelData):
    response = send_email_appointment_cancellation(data)
    if response == "ko":
         return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Error al enviar el email"})
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"message": "Email enviado correctamente"})

@router.post("/send_email_appointment_confirmation")
def send_appointment_confirmation_email(data: EmailAppointmentData):
    response = send_email_appointment_confirmation(data)
    if response == "ko":
         return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Error al enviar el email"})
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"message": "Email enviado correctamente"})