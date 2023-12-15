from sqlalchemy import text
from constants.models import DEFAULT_IMG
from schemas.doctor import  DoctorBase, DoctorCreate, DoctorOut
from models.base import Doctor, User
from schemas.user import UserCreate
from utils import auth

def get_doctors_by_patient_id(db, patient_id: int) -> list[Doctor]:
    query = text("""
                select D.id, U.name + ' ' + U.lastname as full_name, U.phone, U.cc, U.email 
                from doctors D inner join users U
                on D.user_id = U.id inner join doctor_patients DP
                on DP.patient_id = :patient_id AND DP.doctor_id = D.id
                 """)
    
    result = db.execute(query, {'patient_id': patient_id})
    rows = result.fetchall()
    doctors: list[DoctorOut] = []
    for row in rows:
        doctors.append({
            "id": row.id,
            "full_name": row.full_name,
            "phone": row.phone,
            "cc": row.cc,
            "email": row.email
        })
    return doctors

def get_doctors_speciality(db, speciality: str) -> list[Doctor]:
   
    query = text("""select D.id, U.name + ' ' + U.lastname as full_name, U.phone, U.cc, U.email 
                    from doctors D inner join users U
                    on D.user_id = U.id
                    where speciality = :speciality
                """)
    
    result = db.execute(query, {'speciality': speciality})
    rows = result.fetchall()
    
    doctors: list[DoctorOut] = []
    for row in rows:
        doctors.append({
            "id": row.id,
            "full_name": row.full_name,
            "phone": row.phone,
            "cc": row.cc,
            "email": row.email
        })
    return doctors

def get_doctors_patientId(db, patient_id: int) -> list[Doctor]:
   
    query = text("""select D.id, U.name + ' ' + U.lastname as full_name, U.phone, U.cc, U.email 
                    from doctors D inner join users U
                    on D.user_id = U.id
                    where speciality = :patient_id
                """)
    
    result = db.execute(query, {'speciality': speciality})
    rows = result.fetchall()
    
    doctors: list[DoctorOut] = []
    for row in rows:
        doctors.append({
            "id": row.id,
            "full_name": row.full_name,
            "phone": row.phone,
            "cc": row.cc,
            "email": row.email
        })
    return doctors

def create_doctor(doctor: DoctorCreate, db):
    doctor_user_id = create_user_doctor(doctor, db)
    if doctor_user_id:
        doctor_create = DoctorBase(
            speciality=doctor.specialty,
            user_id=doctor_user_id
        )
        doctor_db = create_record_doctor(doctor_create, db)
        return doctor_db
    return None

    

def create_record_doctor(doctor: DoctorBase, db):
    doctor_db = Doctor(**doctor.__dict__)
    db.add(doctor_db)
    db.commit()
    db.refresh(doctor_db)
    return doctor_db

def get_doctor_by_user_id(user_id: int, db):
    doctor = db.query(Doctor).filter(Doctor.user_id == user_id).first()
    return doctor

def create_user_doctor(doctor: DoctorCreate, db):
    user_create = UserCreate(
        name=doctor.name,
        lastname=doctor.lastname,
        email=doctor.email,
        image_url=doctor.image_url,
        password=doctor.password,
        phone=doctor.phone,
        cc=doctor.cc,
        rol_id=doctor.rol_id
    )
    new_user = create_user(user_create, db)
    new_user_id = new_user.id
    return new_user_id

def put_doctor(id: int, doctor: DoctorBase, db):
    print('llegue a editar doctor')
    db_doctor: Doctor = db.query(Doctor).filter(Doctor.id == id).first()
    if db_doctor is None:
        return None
    
    for attr, value in doctor.model_dump().items():
        setattr(db_doctor, attr, value)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

def create_user(new_user: UserCreate, db):
    exist = exist_user(new_user.email, db)
    if exist:
        return None
    
    user = User(**new_user.__dict__)
  
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
    print(email)
    usr = db.query(User).filter(User.email == email).first()
    return usr

def get_doctor_id(db, doctor_id: int) -> DoctorOut:
    query = """ select D.id, U.name + ' ' + U.lastname as full_name, U.phone, U.cc, U.email
                from doctors D inner join users U
                on D.user_id = U.id
                where D.id = :doctor_id"""
                
    result = db.execute(text(query), {'doctor_id': doctor_id})
    row = result.fetchone()
    if row is None:
        return None
    return DoctorOut(id=row.id, full_name=row.full_name, phone=row.phone, cc=row.cc, email=row.email)
    