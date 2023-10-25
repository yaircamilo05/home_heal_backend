from models.base import User
from schemas.user import UserCreate
from models.base import User
from utils.auth import encript_password

def create_user(new_user: UserCreate, db):
    exist = exist_user(new_user.email, db)
    if exist:
        return None
    user = User(**new_user.model_dump())
    # Encriptation of the password
    user.password = encript_password(user.password)
    ## Acá va la logica de consulta en la base de datos
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def exist_user(email: str, db):
    usr = db.query(User).filter(User.email == email).first()
    return usr


def all_users(db):
    return db.query(User).all()
