import math
import random
from fastapi import APIRouter, HTTPException, status
import os
import re
from requests import get

import httpx
import json
from bs4 import BeautifulSoup

from schemas.vital_signs import VitalSignsCreate
from constants.query import *

router = APIRouter()

azure_key = os.environ.get('AZURE_BING_AI_KEY')


@router.post('/az6-search/{user_id}')
def search_6(user_id: int, vs: VitalSignsCreate):
    vs_dict: dict = vs.dict()
    similar_vs = signos_similares(vs)

    combined_info = {}

    for param, value in vs_dict.items():
        sp_params: dict = {
            'heart_rate': 'ritmo cardiaco',
            'blood_pressure': 'presión arterial',
            'O2_saturation': 'saturación de oxígeno'
        }
        query = f"Mejores recomendaciones en salud para {sp_params[param]} con {similar_vs['dx']}, qué hacer?"
        url = "https://api.bing.microsoft.com/v7.0/search"
        headers = {"Ocp-Apim-Subscription-Key": azure_key}
        params = {"q": query, "count": 3}

        try:
            response = get(url, headers=headers, params=params, timeout=30)
        except Exception as e:
            return {"error": f"Error al realizar la solicitud HTTP: {str(e)}"}

        rnd_idx: int = random.randint(0, 2)
        result_url = response.json()["webPages"]["value"][rnd_idx]["url"]

        # Web scraping del sitio mejor calificado
        page = get(result_url)
        soup = BeautifulSoup(page.content, "html.parser")

        # Expresiones regulares ajustadas
        regex_patterns = {
            'heart_rate': re.compile(r"[Pp]uede [^.]*\."),
            'blood_pressure': re.compile(r"[Pp]uede [^.]*\."),
            'O2_saturation': re.compile(r"[Pp]uede [^.]*\.")
        }
        patron = regex_patterns.get(param, None)

        texto_pagina = soup.get_text()
        info_extraida = extraer_datos_salud(texto_pagina, patron)
        texto_limpio = re.sub(r'[^\w\s]', ' ', info_extraida)

        # Eliminar espacios extra y saltos de línea
        texto_limpio = re.sub(r'\s+', ' ', texto_limpio).strip()

        combined_info[param] = texto_limpio

    return combined_info

# @router.post('/az5-search/{user_id}')
# def search_5(user_id: int, vs: VitalSignsCreate):
#     vs_dict: dict = vs.dict()
#     similar_vs = signos_similares(vs)

#     combined_info = {}

#     for param, value in vs_dict.items():
#         sp_params: dict = {
#             'heart_rate': 'ritmo cardiaco',
#             'blood_pressure': 'presión arterial',
#             'O2_saturation': 'saturación de oxígeno'
#         }
#         query = f"Listado recomendaciones si tengo {sp_params[param]} con {similar_vs['dx']}, qué hacer?"
#         url = "https://api.bing.microsoft.com/v7.0/search"
#         headers = {"Ocp-Apim-Subscription-Key": azure_key}
#         params = {"q": query, "count": 1}

#         try:
#             response = get(
#                 url, headers=headers,
#                 params=params, timeout=30
#             )
#         except Exception as e:
#             return {
#                 "error": f"Error al realizar la solicitud HTTP: {str(e)}"
#             }

#         result_url = response.json()["webPages"]["value"][0]["url"]

#         # Web scraping del sitio mejor calificado
#         page = get(result_url)
#         soup = BeautifulSoup(page.content, "html.parser")

#         # Expresiones regulares ajustadas

#         palabras = [palabra for frase in similar_vs['dx']
#                     for palabra in frase.split()]

#         # Unir las palabras con '|'
#         literals = '|'.join(map(re.escape, palabras))+r"[^.]*\."

#         regex_patterns = {
#             'heart_rate': re.compile(
#                 r"(ritmo cardíaco|frecuencia cardíaca) (es|debería ser|puede ser) [^.]*\."
#                 ),
#             'blood_pressure': re.compile(r"(presión arterial|hipertensión) (es|debería ser|puede ser) [^.]*\."),
#             'O2_saturation': re.compile(r"(saturación de oxígeno|niveles de oxígeno) (es|debería ser|puede ser) [^.]*\.")
#         }
#         patron = regex_patterns.get(param, None)

#         texto_pagina = soup.get_text()
#         info_extraida = extraer_datos_salud(texto_pagina, patron)
#         combined_info[param] = info_extraida

#     return ''.join([f'{v}\n' for k, v in combined_info.items()])


@router.post('/consulta-hr/')
def signos_similares(vs: VitalSignsCreate):
    signs = leer_json()

    if not signs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron datos de signos vitales."
        )

    nearest = None
    smaller_distance = float('inf')

    # Iterar sobre la lista para encontrar el objeto más cercano
    for vital_sign in signs:
        distance = math.sqrt(
            + (vital_sign['hr'] - vs.heart_rate) ** 2
            + (vital_sign['O2S'] - vs.O2_saturation) ** 2
            + (vital_sign['bp'] - vs.blood_pressure) ** 2
        )

        if distance < smaller_distance:
            smaller_distance = distance
            nearest = vital_sign

    return {'dx': nearest['Diagnóstico'], 'cx': nearest['Cuidados']}


@router.get('/json-data/')
def leer_json(ruta: str = JSON_DATA_ROUTE):
    with open(ruta, 'r', encoding='utf8') as f:
        data = json.load(f)
    return data


def extraer_datos_salud(texto, patron_regex):
    coincidencias = re.findall(patron_regex, texto)
    # Asegurarse de que todas las coincidencias sean cadenas
    coincidencias = [
        ''.join(coincidencia) if isinstance(
            coincidencia, tuple
        ) else coincidencia for coincidencia in coincidencias
    ]
    return ". ".join(coincidencias[:3]) if coincidencias else "Tu prescripción se ve natural."

# - unused functions - #


# @router.post('/az0-search/{user_id}')
# async def search_0(user_id: int, vs: VitalSignsCreate):
#     query = f'how to improve health with heart rate {vs.heart_rate}, oxygen saturation {vs.O2_saturation}, blood pressure {vs.blood_pressure}'
#     url = 'https://api.bing.microsoft.com/v7.0/search'
#     headers = {'Ocp-Apim-Subscription-Key': azure_key}
#     params = {'q': query}

#     async with httpx.AsyncClient() as client:
#         response = await client.get(
#             url, headers=headers, params=params
#         )
#     return response.json()


# @router.post('/az1-search/{user_id}')
# async def search_1(user_id: int, vs: VitalSignsCreate):
#     vs_dict: dict = vs.dict()
#     combined_info = {}

#     for param, value in vs_dict.items():
#         query = f"best health advice for {param} {value}"
#         url = "https://api.bing.microsoft.com/v7.0/search"
#         headers = {"Ocp-Apim-Subscription-Key": azure_key}
#         # count: 1 para obtener solo el resultado mejor calificado
#         params = {"q": query, "count": 1}

#         async with httpx.AsyncClient() as client:
#             response = await client.get(url, headers=headers, params=params)

#         result_url = response.json()["webPages"]["value"][0]["url"]

#         # Web scraping del sitio mejor calificado
#         page = httpx.get(result_url)
#         soup = BeautifulSoup(page.content, "html.parser")
#         # Aquí necesitas definir cómo extraer la información relevante
#         # Por ejemplo, podrías buscar ciertos elementos o clases específicos
#         info = soup.find(...)  # Implementa tu lógica de extracción aquí

#         # combined_info[param] = info.text if info else "Información no disponible"
#         combined_info[param] = info.text if info else "Información no disponible"

#     return combined_info


# @router.post('/az4-search/{user_id}')
def search(user_id: int, vs: VitalSignsCreate):
    vs_dict: dict = vs.dict()
    combined_info = {}

    for param, value in vs_dict.items():
        sp_params: dict = {
            'heart_rate': 'ritmo cardiaco',
            'blood_pressure': 'presión arterial',
            'O2_saturation': 'saturación de oxígeno'
        }
        query = f"Mejores recomendaciones en salud para {sp_params[param]} de {value}"
        url = "https://api.bing.microsoft.com/v7.0/search"
        headers = {"Ocp-Apim-Subscription-Key": azure_key}
        params = {"q": query, "count": 1}

        try:
            response = get(url, headers=headers, params=params, timeout=30)
        except Exception as e:
            return {"error": f"Error al realizar la solicitud HTTP: {str(e)}"}

        result_url = response.json()["webPages"]["value"][0]["url"]

        # Web scraping del sitio mejor calificado
        page = get(result_url)
        soup = BeautifulSoup(page.content, "html.parser")

        if param == 'O2_saturation':
            print(soup.get_text())

        # Expresiones regulares ajustadas
        regex_patterns = {
            'heart_rate': re.compile(r"[Pp]uede [^.]*\."),
            'blood_pressure': re.compile(r"\d+\..*"),
            'O2_saturation': re.compile(r"\w+(?:,\s*\w+)*\s*:\s*[^.]*\.")
        }
        patron = regex_patterns.get(param, None)

        texto_pagina = soup.get_text()
        info_extraida = extraer_datos_salud(texto_pagina, patron)
        texto_limpio = re.sub(r'[^\w\s]', ' ', info_extraida)

        # Eliminar espacios extra y saltos de línea
        texto_limpio = re.sub(r'\s+', ' ', texto_limpio).strip()

        combined_info[param] = texto_limpio

    return combined_info
