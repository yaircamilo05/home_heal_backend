from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
import requests

from constants.query import *

router = APIRouter()

class SignosVitales(BaseModel):
    heart_rate: int
    blood_pressure: int
    O2_saturation: int

# Endpoint y clave secreta del servicio de diagnóstico
HEALTH_BOT_ENDPOINT = 'https://bot-api-eastus.healthbot.microsoft.com/api/tenants/health-i-aemela6/diagnose'
HEALTH_BOT_SECRET = '6oG8Q~Mj25XWuoSe-qK5avEryTumaWNFvScR1c~L'

@router.post("/query/search/",
             summary="Search the best diagnosis based on the patient actual vital signs (ia implementation).")
async def diagnosticar(signos: SignosVitales):
    try:
        # Preparar los datos para enviar al Health Bot
        datos_para_enviar = {
            "intro": INTRO,
            "signos_vitales": signos.dict(),
            # "data": DATA
        }

        # Envío de los datos al Health Bot
        response = requests.post(
            HEALTH_BOT_ENDPOINT,
            json=datos_para_enviar,
            headers={"Authorization": f"Bearer {HEALTH_BOT_SECRET}"}
        )

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error en el servicio del Health Bot")

        return response.json()

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))