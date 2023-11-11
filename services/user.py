from models.base import User
from schemas.user import UserCreate
from schemas.user import User as UserGet
from models.base import User
from utils import auth
from constants.models import DEFAULT_IMG

def create_user(new_user: UserCreate, db):
    exist = exist_user(new_user.email, db)
    if exist:
        return None
    user = User(**new_user.model_dump())
    if user.file_img == '' or user.file_img is None:
        user.file_img = DEFAULT_IMG

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


def all_users(db) -> list[UserGet]:
    result = []
    users = db.query(User).all();
    for user in users:
        result.append(UserGet(**user.__dict__))
    return result


def put_user(id: int, user: User, db):
    db_user: User = db.query(User).filter(User.id == id).first()
    if db_user is None:
        return None
    for attr, value in user.model_dump().items():
        setattr(db_user, attr, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(id: int, db):
    db_user: User = db.query(User).filter(User.id == id).first()
    if db_user is None:
        return None
    db.delete(db_user)
    db.commit()
    return db_user

