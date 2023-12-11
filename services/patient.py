#service
from datetime import date
from typing import List
from fastapi import HTTPException, UploadFile
from services.vital_signs import create_vital_signs_default_patient
from constants.models import DEFAULT_IMG
from models.base import Doctor, DoctorPatients, Patient, User
from schemas.patient import PatientCard, PatientOut
from schemas.patient import UserRegister
from schemas.user import UserCreate
from schemas.patient import PatientOut as PatientGet
from services.user import create_user
from utils import auth
from sqlalchemy import select, text
from utils import azure

#Register user
def register_user(user: UserRegister, image_file: UploadFile, db) -> Patient:
    """_summary_

    Args:
        user (UserRegister): User brought in from the frontend with all the data from the registration form.
        db (_type_): _data_

    Returns:
        Patient: The patient in case it has been created successfully. In case it has not been created, it returns null to send a bad request from the router section.
    """
    user_patient_id = create_user_patient(user,image_file,db)
    user_familiar_id = create_user_familiar(user,db)


    if user_patient_id and user_familiar_id:
        patient = create_patient(user,user_patient_id,user_familiar_id,db)
    return patient

    return None

#Create user to pacient
def create_user_patient(user: UserRegister, image_file:UploadFile,db) -> int:

    image_url = azure.upload_file_to_azurecontainer(image_file, image_file.filename)

    user_create = UserCreate(
        name = user.name,
        lastname = user.lastname,
        email = user.email,
        image_url = image_url,
        password = user.password,
        phone = user.phone,
        cc = user.cc,
        rol_id = 2
    )

    new_user = create_user(user_create,db)
    new_user_id = new_user.id
    return new_user_id

#Create user to familiar
def create_user_familiar(user: UserRegister,db) -> int:
    user_create = UserCreate(
        name = user.familiar_name,
        lastname = user.familiar_lastname,
        email = user.familiar_email,
        image_url = DEFAULT_IMG,
        password = user.password,
        phone = user.familiar_phone,
        cc = user.cc,
        rol_id = 3
    )
    new_user = create_user(user_create,db)
    new_user_id = new_user.id
    return new_user_id

#Create patient whit user_patient_id and user_familiar_id
def create_patient(user: UserRegister, user_pacient_id: int, user_familiar_id: int ,db):

    patient_create = PatientOut(
        gender = user.gender,
        birthdate = user.birthdate,
        description = user.description,
        address = user.address,
        user_id = user_pacient_id,
        familiar_user_id = user_familiar_id
    )

    patient = Patient(**patient_create.model_dump())

    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


def all_patients(db) -> List[PatientGet]:
    result = []
    patients = db.query(Patient).all()
    for patient in patients:
        try:
            patient_get = PatientGet(
                gender=patient.gender,
                birthdate=patient.birthdate,
                description=patient.description,
                address=patient.address,
                user_id=patient.user_id,
                familiar_user_id=patient.familiar_user_id
            )
            result.append(patient_get)
        except Exception as e:
            # Manejar cualquier error que pueda ocurrir al crear la instancia
            raise HTTPException(status_code=500, detail=f"Error al procesar paciente: {str(e)}")

    return result

def get_patients_by_doctor_id(prm_doctor_id,db):
     # Seleccionar los pacientes y sus usuarios asociados al doctor dado
    query = text("""SELECT 
    P.id, U.name, U.lastname, U.cc, U.phone, U.email, U.image_url,
    P.gender, P.birthdate, P.address, P.description,
    CASE
        WHEN 
            COUNT(VS.id) > 0
            AND (MAX(VS.blood_pressure) >= 36 AND MAX(VS.blood_pressure) <= 37) 
            AND (MAX(VS.hearth_rate) >= 60 AND MAX(VS.hearth_rate) <= 100) 
            AND (MAX(VS.O2_saturation) >= 95)
        THEN 2 -- Estable
        WHEN 
            COUNT(VS.id) > 0
            AND (MAX(VS.blood_pressure) <= 35 OR MAX(VS.blood_pressure) >= 40) 
            OR (MAX(VS.hearth_rate) <= 50 OR MAX(VS.hearth_rate) >= 120) 
            OR (MAX(VS.O2_saturation) <= 85)
        THEN 4 -- Crítico
        WHEN 
            COUNT(VS.id) = 0
        THEN 1 -- Sin signos vitales registrados
        ELSE 3 -- Riesgoso
    END AS status
FROM 
    patients P
    INNER JOIN users U ON P.user_id = U.id
    INNER JOIN doctor_patients DP ON DP.patient_id = P.id
    LEFT JOIN vital_signs VS ON VS.patient_id = P.id AND DP.doctor_id = :prm_doctor_id
GROUP BY 
    P.id, U.name, U.lastname, U.cc, U.phone, U.email, U.image_url,
    P.gender, P.birthdate, P.address, P.description;""")

    result = db.execute(query, {"prm_doctor_id": prm_doctor_id})
    rows = result.fetchall()
    print("RESULTADO DE LA CONSULTA: ", rows)
    # Procesar el resultado para retornar la información deseada
    patients_card: PatientCard = []
    for row in rows:
        patient_card = PatientCard(
            patient_id=row.id,
            name=row.name,
            lastname=row.lastname,
            cc=row.cc,
            email=row.email,
            phone=row.phone,
            address=row.address,
            age = calculate_age_by_birthdate(row.birthdate),
            gender = row.gender,
            img_url=row.image_url,
            description=row.description,
            status= row.status
        )
        patients_card.append(patient_card)

    return patients_card

def calculate_age_by_birthdate(birthdate):
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

def get_patient(patient_id,db) -> PatientCard:
    query = (select(Patient.id,
                    User.name,
                    User.lastname,
                    User.cc,
                    User.phone,
                    User.email,
                    User.image_url,
                    Patient.gender,
                    Patient.birthdate,
                    Patient.address,
                    Patient.description)
            .select_from(Patient)
            .join(User, User.id == Patient.user_id)
            .where(Patient.id == patient_id))
    result = db.execute(query)
    row = result.fetchone()
    patient_card = PatientCard(
            patient_id=row.id,
            name=row.name,
            lastname=row.lastname,
            cc=row.cc,
            email=row.email,
            phone=row.phone,
            address=row.address,
            age = calculate_age_by_birthdate(row.birthdate),
            gender = row.gender,
            description=row.description,
            img_url=row.image_url,
            status= 1)
    return patient_card
