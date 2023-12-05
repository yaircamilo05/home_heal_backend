from fastapi import HTTPException, status
from bs4 import BeautifulSoup
from requests import get
from sqlalchemy.orm import Session
from sqlalchemy import select

from constants.query import JSON_DATA_ROUTE
from models.base import Diagnostic, Doctor, DoctorPatients, Patient
from schemas.diagnostic import DiagnosisCreate, DiagnosisResult
from schemas.vital_signs import VitalSignsCreate

import json
import math
import os
import random
import re


azure_key = os.environ.get('AZURE_BING_AI_KEY')


def vi_searcher(
        pat_id: int, doctor_id: int,
        vs: VitalSignsCreate, db: Session
) -> DiagnosisResult:
    exist_doctor_patient: bool = validate_they_exists(
        doctor_id, pat_id, db
    )
    if not exist_doctor_patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró la relación entre doctor y paciente."
        )

    diagnosis: dict[str:str] = search_engine(vs)

    doc_pat_id = db.query(DoctorPatients).filter(
        DoctorPatients.c.doctor_id == doctor_id,
        DoctorPatients.c.patient_id == pat_id
    ).first().id

    db_diagnosis: Diagnostic = Diagnostic(
        description=f'{diagnosis["heart_rate"]}. {diagnosis["blood_pressure"]}. {diagnosis["O2_saturation"]}.',
        patient_id=pat_id,
        doctor_patients_id=doc_pat_id,
    )
    db.add(db_diagnosis)
    db.commit()
    db.refresh(db_diagnosis)

    return DiagnosisResult(**db_diagnosis.__dict__)


def search_engine(vs: VitalSignsCreate) -> dict[str:str]:
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

    if not combined_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron datos de signos vitales."
        )

    return combined_info


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
    return ". ".join(coincidencias[:3]) if coincidencias else ""


def validate_they_exists(
        doctor_id: int, patient_id: int, db: Session
) -> bool:
    query = (select(
        DoctorPatients
    ).where(
        DoctorPatients.c.doctor_id == doctor_id,
        DoctorPatients.c.patient_id == patient_id
    ))
    result = db.execute(query)
    rows = result.fetchall()
    return True if rows else False
