
from models.base import VitalSign, VitalSignRecord


def create_vital_signs_default_patient(patient_id: int,db):
    ins = VitalSign.__table__.insert().values(
        patient_id=patient_id,
        hearth_rate=0,
        blood_pressure=0,
        O2_saturation=0
    )
    result = db.execute(ins)
    return result

def create_vital_signs(vital_signs: VitalSign,db):
    db.add(vital_signs)
    db.commit()
    db.refresh(vital_signs)
    return vital_signs

def get_history_vital_signs_patient(patient_id: int,db) -> list[VitalSignRecord]:
    vital_signs_history = db.query(VitalSignRecord).filter(VitalSignRecord.patient_id == patient_id).all()
    return vital_signs_history

def get_vital_signs_patient(patient_id: int,db) -> VitalSign:
    vital_signs = db.query(VitalSign).filter(VitalSign.patient_id == patient_id).first()
    return vital_signs