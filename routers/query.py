from fastapi import APIRouter, Depends, HTTPException, status
from models.base import Base

from constants.query import *
import requests


router = APIRouter()


@router.post('/buscar/')
async def buscar(signos: dict):
    headers = {'Ocp-Apim-Subscription-Key': BING_API_KEY}
    # Puedes ajustar el número de resultados con 'count'

    prompt: str = (
        f'{INTRO}{signos.__str__()}.\n{DATA}'
    )

    params = {'q': prompt, 'count': 10}

    try:
        response = requests.get(
            BING_SEARCH_URL, headers=headers, params=params)
        # Esto asegura que se lance una excepción si la solicitud falla
        response.raise_for_status()
        return response.json()  # Devuelve la respuesta JSON de la API de Bing
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
