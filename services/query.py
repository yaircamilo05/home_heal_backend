from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from bs4 import BeautifulSoup
from sqlalchemy import select
from requests import get

from services.vital_signs import get_vital_signs_patient
from models.base import Doctor, DoctorPatients, VitalSigns
from schemas.vital_signs import VitalSignsResponse
from constants.query import JSON_DATA_ROUTE
from schemas.cares import GeneratedCare

import random
import json
import math
import os
import re


azure_key = os.environ.get('AZURE_BING_AI_KEY')


def vi_searcher(
    patient_id: int, user_id: int, db: Session
) -> list[GeneratedCare]:
    doctor_id: int = db.query(Doctor).filter(
        Doctor.user_id == user_id
    ).first().id

    they_exist: bool = validate_they_exists(doctor_id, patient_id, db)
    if not they_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró la relación entre doctor y paciente."
        )

    db_vital_sign: VitalSigns = get_vital_signs_patient(patient_id, db)
    vs_schema: VitalSignsResponse = VitalSignsResponse(
        **db_vital_sign.__dict__
    )

    related_cares: dict[str:str] = search_engine(vs_schema)

    sp_signs: dict[str: str] = {
        'hearth_rate': 'Para el ritmo cardiacto',
        'blood_pressure': 'Para la presión arterial',
        'O2_saturation': 'Para la saturación de oxígeno'
    }

    generatedCares: list[generatedCares] = []
    for key, value in related_cares.items():
        if value == '':
            continue
        newCare: GeneratedCare = GeneratedCare(
            title=sp_signs[key],
            description=value,
            patient_id=patient_id,
            doctor_id=doctor_id
        )
        generatedCares.append(newCare)

    return generatedCares

    # doctor_patient = db.query(DoctorPatients).filter(
    #     DoctorPatients.c.doctor_id ==
    #     diagnostic.doctor_id,  DoctorPatients.c.patient_id == diagnostic.patient_id
    # ).first()
    # if doctor_patient is None:
    #     return None

    # exist_doctor_patient: bool = validate_they_exists(
    #     doctor_id, id, db
    # )
    # if not exist_doctor_patient:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="No se encontró la relación entre doctor y paciente."
    #     )

    # doc_pat_id = db.query(DoctorPatients).filter(
    #     DoctorPatients.c.doctor_id == doctor_id,
    #     DoctorPatients.c.patient_id == id
    # ).first().id

    # db_vital_sign: Diagnostic = Diagnostic(
    #     description=f'{diagnosis["hearth_rate"]}. {diagnosis["blood_pressure"]}. {diagnosis["O2_saturation"]}.',
    #     patient_id=id,
    #     doctor_patients_id=doc_pat_id,
    # )
    # db.add(db_vital_sign)
    # db.commit()
    # db.refresh(db_vital_sign)

    # return DiagnosisResult(**db_vital_sign.__dict__)


def search_engine(vs: VitalSignsResponse) -> dict[str:str]:
    vs_dict: dict = vs.dict()
    similar_vs = signos_similares(vs)

    combined_info = {}

    for param, value in vs_dict.items():
        if param == 'id' or param == 'patient_id':
            continue

        sp_params: dict = {
            'hearth_rate': 'ritmo cardiaco',
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
            'hearth_rate': re.compile(r"[Pp]uede [^.]*\."),
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


def signos_similares(vs: VitalSignsResponse):
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
            + (vital_sign['hr'] - vs.hearth_rate) ** 2
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
