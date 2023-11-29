import os
from constants.models import URL_CHAGUE_PASSWORD
from models.base import User
from schemas.email import EmailLinkData
from schemas.user import RecoveryPassword, UserGetLogin
from services.email import send_link_email_recory_password
from services.rol import get_role
from utils import auth, jwt as jwt
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

def recovery_password(data: RecoveryPassword, db) -> str:
    if not exit_user(data.email, db):
        return False
    user = get_user_by_email(data.email, db)
    user_get = UserGetLogin(**user.__dict__)
    token = jwt.create_token_email(user_get)
    #Enviar el email con el link de recuperacion
    content_email = f"{URL_CHAGUE_PASSWORD}?token={token}"
    data_email:EmailLinkData = EmailLinkData(
        hash=os.environ.get('HASH_VALIDATOR'),
        to_destination=user.email,
        name=user.name,
        link=content_email
    )
    response = send_link_email_recory_password(data_email)
    return response == "ok"

def change_password(token: str, password: str, db) -> bool:
    if not jwt.validate_token(token):
        return False
    user = jwt.validate_token(token)
    user = get_user_by_email(user['email'], db)
    user.password = auth.encript_password(password)
    db.commit()
    return True
