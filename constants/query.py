BING_API_KEY: str = '62893c3e09c54a92b08309330ed6fbba'
BING_SEARCH_URL: str = 'https://api.bing.microsoft.com/v7.0/search'


INTRO: str = 'Responde sobre los principales "diagnosticos" y "cuidados" a tomar. Se te va a dar los signos vitales de un paciente.'

CRITICAL_VS: dict = {
    "heart_rate": 150,
    "blood_pressure": 110,
    "O2_saturation": 88
}

RELAXED_VS: dict = {
    "heart_rate": 60,
    "blood_pressure": 90,
    "O2_saturation": 95
}

JSON_DATA_ROUTE: str = './database/data.json'

MC_LINK: str = [{
    'heart_rate': [
        'https://www.heart.org/en/healthy-living/fitness/fitness-basics/target-heart-rates',
        'https://www.heart.org/en/health-topics/arrhythmia/about-arrhythmia/bradycardia--slow-heart-rate',
        'https://www.heart.org/en/health-topics/arrhythmia/about-arrhythmia/tachycardia--fast-heart-rate',
        'https://www.mayoclinic.org/es/diseases-conditions/tachycardia/symptoms-causes/syc-20355127',
    ],
    'blood_pressure': [
        'https://www.who.int/es/news-room/fact-sheets/detail/hypertension',
        'https://www.heart.org/en/health-topics/high-blood-pressure/understanding-blood-pressure-readings',
        'https://www.mayoclinic.org/es-es/diseases-conditions/high-blood-pressure/symptoms-causes/syc-20373410',
        'https://www.mayoclinic.org/es/diseases-conditions/high-blood-pressure/symptoms-causes/syc-20373410'
    ],
    'O2_saturation': [
        'https://www.mayoclinic.org/es-es/symptoms/hypoxemia/basics/definition/sym-20050930',
        'https://medlineplus.gov/spanish/ency/article/007198.htm',
    ]

}]
DATA: str = (
    f'''A partir del siguiente enlace con documentación médica {MC_LINK} (sólamente documéntate, no debes responder algo explícitamente de dicho documento).
    Encuentra los cuidados y diagnósticos para los signos vitales del paciente.
    Dame una lista de las recomendaciones más prioritarias (de la más importante a las menos importante) de recomendaciones que debería tomar entonces el paciente'''
)
