from models.base import User, Doctor
from schemas.user import UserCreate, UserGet, UserAux, UserUpdate
from schemas.doctor import Doctor as DoctorSchema
from schemas.user import User as UserSchema
from services.doctor import create_doctor, get_doctor_by_user_id, put_doctor
from schemas.rol import RolOut
from models.base import User, Rol
from utils import auth
from constants.models import DEFAULT_IMG
from sqlalchemy import inspect
from sqlalchemy.orm import joinedload
from sqlalchemy import select

def create_user(new_user: UserCreate, db):
    print('llegue a crear usuario')
    exist = exist_user(new_user.email, db)
    if exist:
        return None
    
    user_aux = UserAux(**new_user.__dict__)
    
    user = User(**user_aux.model_dump())
  
    if user.image_url == '' or user.image_url is None:
        user.image_url = DEFAULT_IMG

    # Encriptation of the password
    user.password = auth.encript_password(user.password)
    ## Acá va la logica de consulta en la base de datos

    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    if new_user.specialty != '':
        print('Entre a la creacion del doctor')
        
        print(user.id)
        doctor = DoctorSchema(speciality=new_user.specialty, user_id=user.id)
        
        doctor_bd=create_doctor(doctor, db)
        if doctor_bd is None:
            db.delete(user)
            db.commit()
            return None
    
    return instance_to_dict(user)

def instance_to_dict(instance):
    return {c.key: getattr(instance, c.key) for c in inspect(instance).mapper.column_attrs}

def exist_user(email: str, db):
    print(email)
    usr = db.query(User).filter(User.email == email).first()
    return usr


def all_users(db) -> list[UserGet]:
    result = []
    users = db.query(User).options(joinedload(User.rol)).all()
    speciality = ''
    
    for user in users:
        try:
            doctor:Doctor = get_doctor_by_user_id(user.id,db)
            if doctor is not None:
                speciality = doctor.speciality
            result.append(UserGet(**instance_to_dict(user), rol=RolOut(**instance_to_dict(user.rol)), specialty=speciality))
        except Exception as e:
            print(e)
            continue
    return result


def put_user(id: int, user: UserCreate, db):
    print('entre a la modificacion del usuario')
    db_user: User = db.query(User).filter(User.id == id).first()
    medico: Doctor = db.query(Doctor).filter(Doctor.user_id == id).first()
    if (medico is not None):
        print('entre a la modificacion del doctor')
        doc= put_doctor(medico.id, DoctorSchema(speciality=user.specialty, user_id=db_user.id), db)
        if doc is None:
            return None  
    if db_user is None:
        return None
    ##user_aux = UserSchema(**user.model_dump())
    for attr, value in user.model_dump().items():
        print('Entre a la modificacion del usuario(cilo)')
        setattr(db_user, attr, value)
    db.commit()
    db.refresh(db_user)
    return instance_to_dict(db_user)


def delete_user(id: int, db):
    db_user: User = db.query(User).filter(User.id == id).first()
    medico: Doctor = db.query(Doctor).filter(Doctor.user_id == id).first()
    if (medico is not None):
        db.delete(medico)
        db.commit()
    if db_user is None:
        return None
    db.delete(db_user)
    db.commit()
    return db_user

