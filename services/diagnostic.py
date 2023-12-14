from sqlalchemy.orm import joinedload
from models.base import DoctorPatients, Diagnostic, Doctor
from schemas.diagnostic import DiagnosticCreate


def create_diagnostic(diagnostic: DiagnosticCreate, db):
    doctor_patient = db.query(DoctorPatients).filter(DoctorPatients.c.doctor_id == diagnostic.doctor_id,  DoctorPatients.c.patient_id == diagnostic.patient_id).first()
    if doctor_patient is None:
        return None
    diagnostic_bd = Diagnostic(description=diagnostic.description, doctor_patients_id=doctor_patient.id, patient_id= diagnostic.patient_id)
    db.add(diagnostic_bd)
    db.commit()
    db.refresh(diagnostic_bd)
    return diagnostic_bd


def get_diagnostic_by_patient_id(id:int, db):
    diagnostics_bd: Diagnostic=db.query(Diagnostic).options(joinedload(Diagnostic.doctor).joinedload(Doctor.user)).join(DoctorPatients, Diagnostic.doctor_patients_id == DoctorPatients.c.id).filter(DoctorPatients.c.patient_id == id).all()
    for diagnostic in diagnostics_bd:
        diagnostic.doctor[0].user.password = None
    return diagnostics_bd


def delete_diagnostic(id:int, db) -> bool:
    diagnostic = db.query(Diagnostic).filter(Diagnostic.id == id).first()
    if diagnostic:
        db.delete(diagnostic)
        db.commit()
        return True
    return False