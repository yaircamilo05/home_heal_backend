from constants.models import DEFAULT_IMG
from models.base import Patient, User
from schemas.pacient import PacientOut
from schemas.pacient import UserRegister
from schemas.user import UserCreate
from utils import auth

def register_user(user: UserRegister,db):
    user_pacient_id = create_user_pacient(user,db)
    user_familiar_id = create_user_familiar(user,db)
   
    if user_pacient_id and user_familiar_id:
        return create_pacient(user,user_pacient_id,user_familiar_id,db)
    
    return None

def create_user_pacient(user: UserRegister,db):
    user_create = UserCreate(
        name = user.name,
        lastname = user.lastname,
        email = user.email,
        image_url = DEFAULT_IMG,
        password = user.password,
        rol_id = 2
    )
    return create_user(user_create,db)

def create_user_familiar(user: UserRegister,db) -> User:
    user_create = UserCreate(
        name = user.familiar_name,
        lastname = user.familiar_lastname,
        email = user.familiar_email,
        image_url = DEFAULT_IMG,
        password = user.password,
        rol_id = 3
    )
    return create_user(user_create,db)

def create_pacient(user: UserRegister, user_familiar_id: int, user_pacient_id: int ,db):
    patient_create = Patient(
        gender = user.gender,
        date_of_birth = user.date_of_birth,
        description = user.description,
        address = user.address,
        user_id = user_pacient_id,
        familiar_user_id = user_familiar_id
    )
    return PacientOut(**patient_create.__dict__)
    
def create_user(new_user: UserCreate, db):
    exist = exist_user(new_user.email, db)
    if exist:
        return None
    user = User(**new_user.model_dump())
    if user.image_url == '' or user.image_url is None:
        user.image_url = DEFAULT_IMG

    # Encriptation of the password
    user.password = auth.encript_password(user.password)
    ## Acá va la logica de consulta en la base de datos
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def exist_user(email: str, db):
    usr = db.query(User).filter(User.email == email).first()
    return usr