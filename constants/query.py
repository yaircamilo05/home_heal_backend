BING_API_KEY: str = '62893c3e09c54a92b08309330ed6fbba'
BING_SEARCH_URL: str = 'https://api.bing.microsoft.com/v7.0/search'


INTRO: str = 'Responde sobre los principales "diagnosticos" y "cuidados". Se te va a dar que los signos vitales del paciente son:\n'

CRITICAL_VS: dict = {
    "heart_rate": 150,
    "blood_pressure": 110,
    "O2_saturation": 88
}

RELAXED_VS: dict = {
    'heart_rate': 60,  # Frecuencia cardíaca muy baja (bradicardia)
    # Presión arterial muy baja (hipotensión severa)
    'blood_pressure': (90, 60),
    'O2_saturation': 95  # Saturación de oxígeno baja
}

MC_LINK: str = 'https://www.mayoclinic.org/es-es/symptoms'
DATA: str = (
    f'''A partir del siguiente enlace con documentación médica {MC_LINK}.
    Encuentra los cuidados y diagnósticos para los signos vitales del paciente.'''
)
