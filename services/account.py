from models.base import User
from schemas.user import UserGetLogin
from services.rol import get_role
from utils import auth, jwt
from schemas.login import credentials_login
from services.rol_menu import get_menus_role
from fastapi.encoders import jsonable_encoder


def login(credentials: credentials_login, db) -> str:
    if not exit_user(credentials.email, db):
        return None
    user = get_user_by_email(credentials.email, db)
    if user and auth.check_password(credentials.password, user.password):
        user_get = UserGetLogin(**user.__dict__)
        token = jwt.create_token(user_get)
    return token


def validate_token(token: str, db) -> dict:
    data_token = jwt.validate_token(token)
    # Retorno de diccionario con los datos del token y el usuario
    menu_roles = get_menus_role(db, data_token['rol_id'])
    rol = get_role(data_token['rol_id'], db)
    data_token['menus'] = jsonable_encoder(menu_roles)
    data_token['rol'] = jsonable_encoder(rol)
    if not data_token:
        return None
    return data_token


def exit_user(email: str, db) -> bool:
    user = get_user_by_email(email, db)
    return user != None


def get_user_by_email(email: str, db) -> User:
    user = db.query(User).filter(User.email == email).first()
    return user
