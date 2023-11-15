#service
from constants.models import DEFAULT_IMG
from models.base import Patient, User
from schemas.patient import PatientOut
from schemas.patient import UserRegister
from schemas.user import UserCreate
from schemas.patient import PatientOut as PatientGet
from services.user import create_user
from utils import auth

#Register user
def register_user(user: UserRegister,db) -> Patient:
    """_summary_

    Args:
        user (UserRegister): User brought in from the frontend with all the data from the registration form.
        db (_type_): _data_

    Returns:
        Patient: The patient in case it has been created successfully. In case it has not been created, it returns null to send a bad request from the router section.
    """
    user_patient_id = create_user_pacient(user,db)
    user_familiar_id = create_user_familiar(user,db)
   
    if user_patient_id and user_familiar_id:
        return create_pacient(user,user_patient_id,user_familiar_id,db)
    
    return None

#Create user to pacient
def create_user_pacient(user: UserRegister,db) -> int:
    user_create = UserCreate(
        name = user.name,
        lastname = user.lastname,
        email = user.email,
        image_url = user.image_url,
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
        image_url = user.image_url,
        password = user.password,
        phone = user.familiar_phone,
        cc = '',
        rol_id = 3
    )
    new_user = create_user(user_create,db)
    new_user_id = new_user.id
    return new_user_id

#Create pacient whit user_pacient_id and user_familiar_id
def create_pacient(user: UserRegister, user_familiar_id: int, user_pacient_id: int ,db):
    
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

#Get all patients
def all_patients(db) -> list[PatientGet]:
    result = []
    patients = db.query(Patient).all();
    for patient in patients:
        result.append(PatientGet(**Patient.__dict__))
    return result