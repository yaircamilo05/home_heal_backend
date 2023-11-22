
from models.base import VitalSign, VitalSignRecord


def create_vital_signs_default_patient(patient_id: int,db):
    vital_signs_create = VitalSign(
        patient_id = patient_id,
        hearth_rate = 0,
        blood_pressure = 0,
        O2_saturation = 0
    )
    new_vital_signs = create_vital_signs(vital_signs_create,db)
    return new_vital_signs

def create_vital_signs(vital_signs: VitalSign,db):
    db_vital_signs = VitalSign(
        hearth_rate = vital_signs.hearth_rate,
        blood_pressure = vital_signs.blood_pressure,
        O2_saturation = vital_signs.O2_saturation,
        patient_id = vital_signs.patient_id
    )
    db.add(db_vital_signs)
    db.commit()
    db.refresh(db_vital_signs)
    return db_vital_signs

def get_history_vital_signs_patient(patient_id: int,db) -> list[VitalSignRecord]:
    vital_signs_history = db.query(VitalSignRecord).filter(VitalSignRecord.patient_id == patient_id).all()
    return vital_signs_history

def get_vital_signs_patient(patient_id: int,db) -> VitalSign:
    vital_signs = db.query(VitalSign).filter(VitalSign.patient_id == patient_id).first()
    return vital_signs